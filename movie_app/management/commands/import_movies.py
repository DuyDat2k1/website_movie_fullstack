import requests
import time
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from movie_app.models import Movie, Genre, Country, Episode

OPHIM_API = "https://ophim1.com"
PATH_IMAGE = "https://img.ophim.live/uploads/movies/"


def get_or_create_genre(name):
    genre, _ = Genre.objects.get_or_create(name=name)
    return genre


def get_or_create_country(name):
    country, _ = Country.objects.get_or_create(name=name)
    return country


class Command(BaseCommand):
    help = "Import movies from OPHim API"

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=5, help='Number of pages to import')
        parser.add_argument('--all', action='store_true', help='Import all pages')
        parser.add_argument('--slug', type=str, help='Import a specific movie by slug')

    def handle(self, *args, **options):
        if options['slug']:
            self.import_single(options['slug'])
            return

        page = 1
        max_pages = 9999 if options['all'] else options['pages']

        while page <= max_pages:
            self.stdout.write(f"Fetching page {page}...")
            try:
                res = requests.get(f"{OPHIM_API}/danh-sach/phim-moi-cap-nhat?page={page}", timeout=30)
                data = res.json()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching page {page}: {e}"))
                break

            items = data.get('items', [])
            if not items:
                break

            for item in items:
                self.import_movie(item['slug'])

            total_pages = data.get('pagination', {}).get('totalPages', 1)
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.3)

    def import_single(self, slug):
        self.import_movie(slug)

    def import_movie(self, slug):
        try:
            res = requests.get(f"{OPHIM_API}/phim/{slug}", timeout=30)
            data = res.json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching {slug}: {e}"))
            return

        movie_data = data.get('movie')
        if not movie_data:
            return

        ophim_id = movie_data.get('_id', '')
        name = movie_data.get('name', '')
        origin_name = movie_data.get('origin_name', '')
        content = movie_data.get('content', '')
        year = movie_data.get('year', 0)
        quality = movie_data.get('quality', 'HD')
        view = movie_data.get('view', 0)
        episode_current = movie_data.get('episode_current', '')
        episode_total = movie_data.get('episode_total', '1')

        thumb_url = movie_data.get('thumb_url', '')
        poster_url = movie_data.get('poster_url', '')
        if thumb_url and not thumb_url.startswith('http'):
            thumb_url = PATH_IMAGE + thumb_url
        if poster_url and not poster_url.startswith('http'):
            poster_url = PATH_IMAGE + poster_url

        type_str = movie_data.get('type', 'single')
        chieurap = movie_data.get('chieurap', False)

        if chieurap:
            movie_type = Movie.MovieType.CINEMA
        elif type_str == 'series':
            movie_type = Movie.MovieType.SERIES
        elif type_str == 'hoathinh' or type_str == 'animation':
            movie_type = Movie.MovieType.ANIMATION
        else:
            movie_type = Movie.MovieType.SINGLE

        # Map quality
        quality_map = {
            'HD': Movie.Quality.HD,
            'Vietsub': Movie.Quality.VIETSUB,
            'Thuyết Minh': Movie.Quality.THUYET_MINH,
            'Lồng Tiếng': Movie.Quality.LONG_TIENG,
        }
        quality_enum = quality_map.get(quality, Movie.Quality.HD)

        # Strip HTML from content
        import re
        clean_content = re.sub(r'<[^>]+>', '', content).strip()

        # Parse episode count
        ep_count = None
        if episode_total and episode_total.isdigit():
            ep_count = int(episode_total)
        elif episode_total == '1' or episode_current == 'Full':
            ep_count = 1

        movie, created = Movie.objects.update_or_create(
            slug=slug,
            defaults={
                'ophim_id': ophim_id,
                'title': name,
                'title_original': origin_name,
                'description': clean_content,
                'poster': poster_url,
                'thumb': thumb_url,
                'release_year': year,
                'movie_type': movie_type,
                'quality': quality_enum,
                'episode_count': ep_count,
                'views': view,
            }
        )

        # Handle country
        country_data = movie_data.get('country', [])
        if country_data:
            country_name = country_data[0].get('name', '')
            if country_name:
                movie.country = get_or_create_country(country_name)

        # Handle genres
        category_data = movie_data.get('category', [])
        if category_data:
            movie.genres.clear()
            for cat in category_data:
                genre_name = cat.get('name', '')
                if genre_name:
                    genre = get_or_create_genre(genre_name)
                    movie.genres.add(genre)

        movie.save()

        # Update episodes
        episodes_data = data.get('episodes', [])
        if episodes_data:
            movie.episodes.all().delete()
            sort_order = 0
            for server in episodes_data:
                server_name = server.get('server_name', 'Vietsub')
                server_items = server.get('server_data', [])
                for ep in server_items:
                    ep_name = ep.get('name', 'Full')
                    ep_slug = ep.get('slug', slugify(ep_name))
                    link_embed = ep.get('link_embed', '')
                    link_m3u8 = ep.get('link_m3u8', '')

                    ep_num = 0
                    if ep_name.lower() == 'full':
                        ep_num = 1
                    elif ep_name.isdigit():
                        ep_num = int(ep_name)

                    Episode.objects.create(
                        movie=movie,
                        server_name=server_name,
                        name=ep_name,
                        slug=ep_slug,
                        link_embed=link_embed,
                        link_m3u8=link_m3u8,
                        episode_number=ep_num,
                        sort_order=sort_order,
                    )
                    sort_order += 1

        action = "Imported" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action}: {name} ({slug})"))
