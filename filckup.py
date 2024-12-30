
import logging
import sys
from phockup import parse_args, setup_logging
from src.dependency import check_dependencies
from src.filckup import Filckup

__version__ = '1.0.0'

PROGRAM_DESCRIPTION = """\
Media sorting tool to organize files in folders by year, \
month and day.
The software will collect all files from the input directory and copy them to the output
directory without changing the files content. It will only rename the files and place
them in the proper directory for year, month and day.
"""

logger = logging.getLogger('filckup')


def main(options):
    check_dependencies()

    return Filckup(
        options.input_dir,
        options.output_dir,
        dir_format=options.date,
        move=options.move,
        link=options.link,
        date_regex=options.regex,
        original_filenames=options.original_names,
        timestamp=options.timestamp,
        date_field=options.date_field,
        dry_run=options.dry_run,
        quiet=options.quiet,
        progress=options.progress,
        max_depth=options.maxdepth,
        file_type=options.file_type,
        max_concurrency=options.max_concurrency,
        no_date_dir=options.no_date_dir,
        skip_unknown=options.skip_unknown,
        movedel=options.movedel,
        rmdirs=options.rmdirs,
        output_prefix=options.output_prefix,
        output_suffix=options.output_suffix,
        from_date=options.from_date,
        to_date=options.to_date
    )


if __name__ == '__main__':
    try:
        options = parse_args()
        setup_logging(options)
        main(options)
    except Exception as e:
        logger.warning(e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error("Exiting filckup...")
        sys.exit(1)
    sys.exit(0)
