import os
import sys
import time
import argparse
start_time = time.time()

from starrail.entrypoints.entrypoint_handler import StarRailEntryPointHandler
from starrail.entrypoints.help_format_handler import HelpFormatHandler
from starrail.utils.utils import aprint, verify_platform, is_admin, Printer, color_cmd
from starrail.constants import COMMAND, DEVELOPMENT
from starrail.exceptions.exceptions import StarRailOSNotSupported, SRExit


class StarRailArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = []

    def add_group(self, title, description=None):
        group = {'title': title, 'description': description, 'parsers': []}
        self.groups.append(group)
        return group

    def add_parser_to_group(self, group, parser):
        group['parsers'].append(parser)
        
    def error(self, message):
        if "invalid choice:" in message:
            command = message.split("'")[1]
            helpt = Printer.to_purple("starrail help")
            aprint(f"Command not recognized: {command}\nType '{helpt}' for the commands list")
        else:
            parts = message.split("'")
            if len(parts) > 1:
                command = parts[1]
                helpt = Printer.to_purple(f"{command} --help")
                aprint(f"{message.capitalize()}\nType '{helpt}' for its arguments list")
            else:
                helpt = Printer.to_purple("<command> --help")
                aprint(f"{message.capitalize()}\nType '{helpt}' for its arguments list")
        
        self.exit(2)


def start_starrail():
    os.system("")  # Enables ANSI escape characters in terminal
    
    entrypoint_handler = StarRailEntryPointHandler()
    help_format_handler = HelpFormatHandler()
    
    parser = StarRailArgParser(prog=COMMAND, description="StarRail CLI Module")
    subparsers = parser.add_subparsers(dest='command', help='commands')

    help_parser = subparsers.add_parser('help', help='Show this help message and exit')
    help_parser.set_defaults(func=lambda args: help_format_handler.print_help(args, parser))


    # ================================================
    # ==================| PROJECT | ==================
    # ================================================
    
    about_group = parser.add_group('Package Info', 'Get information about the starrail package.')
    
    abt_parser = subparsers.add_parser('about', help='Verbose all information about this module', description='Verbose all information about this module')
    abt_parser.set_defaults(func=entrypoint_handler.about)
    parser.add_parser_to_group(about_group, abt_parser)
    
    version_parser = subparsers.add_parser('version', help='Verbose game AND module version', description='Verbose game AND module version')
    version_parser.set_defaults(func=entrypoint_handler.version)
    parser.add_parser_to_group(about_group, version_parser)
    
    repo_parser = subparsers.add_parser('repo', help='Verbose module repository link', description='Verbose module repository link')
    repo_parser.add_argument('--open', '-o', action='store_true', default=False, help='Open repository in web.')
    repo_parser.set_defaults(func=entrypoint_handler.repo)
    parser.add_parser_to_group(about_group, repo_parser)
    
    author_parser = subparsers.add_parser('author', help='Verbose module author', description='Verbose module author')
    author_parser.set_defaults(func=entrypoint_handler.author)
    parser.add_parser_to_group(about_group, author_parser)
    
    
    # ================================================
    # =================| GAME INFO | =================
    # ================================================
    
    game_info_group = parser.add_group('Game Info', 'Get static and realtime information about the local installation of Honkai: Star Rail.')
    
    show_status = subparsers.add_parser('status', help='Show real-time game status (game process)', description='Show real-time game status (game process)')
    show_status.add_argument('--live', '-l', action='store_true', default=False, help='Show live game status (non-stop).')
    show_status.set_defaults(func=entrypoint_handler.show_status)
    parser.add_parser_to_group(game_info_group, show_status)
    
    show_config = subparsers.add_parser('config', help='Show game configuration in the starrail module', description='Show game configuration in the starrail module')
    show_config.set_defaults(func=entrypoint_handler.show_config)
    parser.add_parser_to_group(game_info_group, show_config)

    details_config = subparsers.add_parser('details', help='Show detailed information about the game and the client', description='Show detailed information about the game and the client')
    details_config.set_defaults(func=entrypoint_handler.show_details)
    parser.add_parser_to_group(game_info_group, details_config)

    pt_config = subparsers.add_parser('runtime', help='Show time in hour, minutes, and seconds since this game session has started', description='Show time in hour, minutes, and seconds since this game session has started')
    pt_config.set_defaults(func=entrypoint_handler.play_time)
    parser.add_parser_to_group(game_info_group, pt_config)


    # =================================================
    # ===============| LAUNCH DRIVER | ================
    # =================================================

    apps_group = parser.add_group('Start/Stop Commands', 'Start/Stop or schedule Honkai: Star Rail application from the CLI.')
    
    start_parser = subparsers.add_parser('start', help='Start the Honkai: Star Rail application', description='Start the Honkai: Star Rail application')
    start_parser.set_defaults(func=entrypoint_handler.start)
    parser.add_parser_to_group(apps_group, start_parser)
    
    stop_parser = subparsers.add_parser('stop', help='Terminate the Honkai: Star Rail application', description='Terminate the Honkai: Star Rail application')
    stop_parser.set_defaults(func=entrypoint_handler.stop)
    parser.add_parser_to_group(apps_group, stop_parser)
    
    schedule_parser = subparsers.add_parser('schedule', help='Schedule the start/stop of the application at a given time', description='Schedule the start/stop of the application at a given time')
    schedule_parser.add_argument('subcommand', nargs='?', default=None, help='add / remove / show')
    schedule_parser.add_argument('--action', type=str, default="start", help='Specify start or stop (only needed for schedule add)')
    schedule_parser.add_argument('--time', type=str, help='Specify the scheduled time (only needed for schedule add) (i.e. 10:30)')
    schedule_parser.set_defaults(func=entrypoint_handler.schedule)
    parser.add_parser_to_group(apps_group, schedule_parser)

    
    # =================================================
    # =================| AUTOMATION | =================
    # =================================================
    
    auto_group = parser.add_group('Automation Commands', 'Simple automation for automating Honkai: Star Rail\'s gameplay.')
    
    auto_parser = subparsers.add_parser('automation', help='', description='')
    auto_parser.add_argument('action', nargs='?', default=None, help='record / run / show / remove / clear')
    auto_parser.set_defaults(func=entrypoint_handler.automation)
    parser.add_parser_to_group(auto_group, auto_parser)
    
    click_parser = subparsers.add_parser('click', help='Continuously click mouse based on given interval.', description='Continuously click mouse based on given interval.')
    click_parser.add_argument('--clicks', '-c', type=int, default=-1, help='Number of clicks. Leave empty (default) to run forever')
    click_parser.add_argument('--interval', '-i', type=float, default=1, help='Interval delay (seconds) between clicks')
    click_parser.add_argument('--randomize', '-r', type=float, default=1.0, help='Randomize the click interval by added 0 to x seconds to the interval specification.')
    click_parser.add_argument('--hold', type=float, default=0.1, help='Delay (seconds) between click press and release')
    click_parser.add_argument('--delay', '-d', type=float, default=3, help='Delay (seconds) before the clicks start')
    click_parser.add_argument('--quiet', '-q', action='store_true', default=False, help='Run without verbosing progress')
    click_parser.set_defaults(func=entrypoint_handler.click_continuously)
    parser.add_parser_to_group(auto_group, click_parser)
    
    
    # =================================================
    # ==================| KEY URLS | ==================
    # =================================================
    
    url_group = parser.add_group('Official Pages', "Access official Honkai: Star Rail's web pages from the CLI")
    
    homepage_parser = subparsers.add_parser('homepage', help='Open the official home page of Honkai: Star Rail', description='Open the official home page of Honkai: Star Rail')
    homepage_parser.add_argument('-cn', action='store_true', default=False, help='Open CN version of the home page.')
    homepage_parser.set_defaults(func=entrypoint_handler.homepage)
    parser.add_parser_to_group(url_group, homepage_parser)
    
    hoyolab_parser = subparsers.add_parser('hoyolab', help='Open the HoyoLab page of Honkai: Star Rail', description='Open the HoyoLab page of Honkai: Star Rail')
    hoyolab_parser.set_defaults(func=entrypoint_handler.hoyolab)
    parser.add_parser_to_group(url_group, hoyolab_parser)
    
    youtube_parser = subparsers.add_parser('youtube', help='Open the official Youtube page of Honkai: Star Rail', description='Open the official Youtube page of Honkai: Star Rail')
    youtube_parser.set_defaults(func=entrypoint_handler.youtube)
    parser.add_parser_to_group(url_group, youtube_parser)
    
    bilibili_parser = subparsers.add_parser('bilibili', help='Open the official BiliBili page of Honkai: Star Rail', description='Open the official BiliBili page of Honkai: Star Rail')
    bilibili_parser.set_defaults(func=entrypoint_handler.bilibili)
    parser.add_parser_to_group(url_group, bilibili_parser)
    
    
    # =================================================
    # =============| UTILITY FUNCTIONS | ==============
    # =================================================

    utility_group = parser.add_group('Utility Commands', 'Honkai: Star Rail utility features directly from the CLI.')

    sc_config = subparsers.add_parser('screenshots', help='Open the screenshots directory in File Explorer', description='Open the screenshots directory in File Explorer')
    sc_config.set_defaults(func=entrypoint_handler.screenshots)
    parser.add_parser_to_group(utility_group, sc_config)
    
    logs_config = subparsers.add_parser('game-logs', help='Open the games log directory in File Explorer', description='Open the games log directory in File Explorer')
    logs_config.set_defaults(func=entrypoint_handler.game_logs)
    parser.add_parser_to_group(utility_group, logs_config)
    
    decode_config = subparsers.add_parser('decode', help='Decode ASCII-based binary files', description='Decode ASCII-based binary files')
    decode_config.add_argument('--path', type=str, default=None, help='Path of the binary file to decode.')
    decode_config.add_argument('--min-length', type=int, default=8, help='Minimum ASCII length to be considered as a valid string.')
    decode_config.set_defaults(func=entrypoint_handler.decode)
    parser.add_parser_to_group(utility_group, decode_config)
    
    pulls_config = subparsers.add_parser('pulls', help='View the pull history page directly in the browser', description='View the pull history page directly in the browser')
    pulls_config.set_defaults(func=entrypoint_handler.pulls)
    parser.add_parser_to_group(utility_group, pulls_config)
    
    cache_announcement_config = subparsers.add_parser('webcache', help='Show decoded web cache URLs (events, pulls, announcements)', description='Show decoded web cache URLs (events, pulls, announcements)')
    cache_announcement_config.add_argument('--announcements', '-a', action='store_true', default=False, help='Show cached announcements.')
    cache_announcement_config.add_argument('--events', '-e', action='store_true', default=False, help='Show cached events.')
    cache_announcement_config.add_argument('--quiet', '-q', action='store_true', default=False, help='Do not verbose web cache explanation.')
    cache_announcement_config.add_argument('--open', action='store_true', default=False, help='Open all web cache URLs found.')
    cache_announcement_config.set_defaults(func=entrypoint_handler.webcache)
    parser.add_parser_to_group(utility_group, cache_announcement_config)
    


    # =================================================
    # ==========| BASE CONFIGURATION CMD | ============
    # =================================================
    
    app_utility_group = parser.add_group('Configure Commands', 'Configure (auto-locate) and Honkai: Star Rail on the local machine. Must be ran before anything else.')
    
    sync_parser = subparsers.add_parser('configure', help='Configure the starrail module on the local machine (auto-locate the Star Rail application). ', description="Configure the starrail module on the local machine (auto-locate the Star Rail application).")
    sync_parser.set_defaults(func=entrypoint_handler.configure)
    parser.add_parser_to_group(app_utility_group, sync_parser)
    
    
    # =================================================
    # ==============| HELPER FUNCTIONS | ==============
    # =================================================
    
    module_utility_group = parser.add_group('Helper Commands', '')
    
    elev_parser = subparsers.add_parser('elevate', help=f'Request {COMMAND} to be ran as admin.', description=f'Request {COMMAND} to be ran as admin.')
    elev_parser.add_argument('arguments', nargs='*', default=[], help=f'Any arguments to be followed after `{COMMAND}`')
    elev_parser.set_defaults(func=entrypoint_handler.elevate)
    parser.add_parser_to_group(module_utility_group, elev_parser)
    
    
    # ================================================
    # ==================| FIREFLY | ==================
    # ================================================
    ff_group = parser.add_group('???', 'What could this be?')
    
    ff_parser = subparsers.add_parser('FIREFLY')
    ff_parser.set_defaults(func=entrypoint_handler.firefly)
    parser.add_parser_to_group(ff_group, ff_parser)
    
    
    # ===========================================================================================
    # >>> BLOCKING FUNCTIONS
    # ===========================================================================================
    if verify_platform() == False:
        raise StarRailOSNotSupported()
    
    module_fully_configured = entrypoint_handler.star_rail.config.full_configured()
    if not module_fully_configured:
        # If the module is not fully configured, then force user to first configure the module
        def blocked_func(args):
            text = color_cmd('starrail configure')
            aprint(f"The StarRail module is not fully configured to run on this machine.\nTo configure the module, run `{text}`")
            raise SRExit()

        for name, subparser in subparsers.choices.items():
            if name not in ["configure", "version", "author", "repo"]:
                subparser.set_defaults(func=blocked_func)
    
    
    # isadmin = is_admin()
    # if not isadmin:
    #     # Certain commands require admin permissions to execute
    #     def blocked_func(args):
    #         elevate_cmd = color_cmd("amiya elevate", with_quotes=True)
    #         aprint(f"Insufficient permission. Run {elevate_cmd} to elevate permissions first.")
    #         raise SRExit()

    #     for name, subparser in subparsers.choices.items():
    #         if name in ["record-auto", "run-auto"]:
    #             subparser.set_defaults(func=blocked_func)
    
    
    # ===========================================================================================
    # >>> PARSER DRIVER
    # ===========================================================================================
    
    # Check if no command line arguments are provided
    if len(sys.argv) == 1:
        aprint("Loading starrail CLI environment...")
        entrypoint_handler.start_cli(parser)
    else:
        # Normal command line execution
        args = parser.parse_args()
        if hasattr(args, 'func'):
            try:
                args.func(args)
            except KeyboardInterrupt:
                aprint("Keyboard Interrupt! StarRail Exiting.")
            except SRExit:
                exit()
        else:
            parser.print_help()
