import readline
import argparse
import getpass
import webbrowser
import tabulate
import subprocess

from starrail.constants import BASENAME, AUTHOR, VERSION, VERSION_DESC, AUTHOR_DETAIL, REPOSITORY, CURSOR_UP_ANSI, REPOSITORY, STARRAIL_DIRECTORY, ISSUES
from starrail.utils.utils import *
from starrail.utils.binary_decoder import  StarRailBinaryDecoder
from starrail.utils.game_detector import StarRailGameDetector
from starrail.utils.perm_elevate import StarRailPermissionsHandler
from starrail.exceptions.exceptions import SRExit, StarRailBaseException

from starrail.controllers.star_rail_app import HonkaiStarRail
from starrail.controllers.web_controller import StarRailWebController
from starrail.controllers.automation_controller import StarRailAutomationController
from starrail.controllers.c_click_controller import ContinuousClickController

from starrail.bin.loader.loader import Loader
from starrail.bin.scheduler.starrail_scheduler import StarRailScheduler, OperationTypes


class StarRailEntryPointHandler:
    def __init__(self):
        self.star_rail              = HonkaiStarRail()
        self.web_controller         = StarRailWebController()
        self.scheduler              = StarRailScheduler(self.star_rail) # Only the start/stop is used from the starrail instance
        self.automation_controller  = StarRailAutomationController(self.star_rail)
    
    
    # ================================================
    # ==================| PROJECT | ==================
    # ================================================
    def about(self, args):
        headers = [Printer.to_lightblue(title) for title in ["Title", "Description"]]
        data = [
            ["Module",      BASENAME],
            ["Version",     f"{VERSION_DESC}-{VERSION}"],
            ["Author",      AUTHOR],
            ["Repository",  REPOSITORY],
            ["Directory",   STARRAIL_DIRECTORY]
        ]
        for row in data:
            row[0] = Printer.to_lightpurple(row[0])
        print("\n" + tabulate.tabulate(data, headers=headers) + "\n")
    
    def version(self, args):
        headers = [Printer.to_lightblue(title) for title in ["Program", "Description", "Version"]]
        data = [
            ["Honkai: Star Rail", "Game", self.star_rail.fetch_game_version()],
            [BASENAME, "Module", f"{VERSION_DESC}-{VERSION}"]
        ]
        for row in data:
            row[0] = Printer.to_lightpurple(row[0])
        print("\n" + tabulate.tabulate(data, headers=headers) + "\n")

    def author(self, args):
        aprint(AUTHOR_DETAIL)
    
    def repo(self, args):
        aprint(REPOSITORY)
        if args.open:
            webbrowser.open(REPOSITORY)

    
    # =================================================
    # ==================| GAME INFO | =================
    # =================================================
    
    def show_status(self, args):
        self.star_rail.show_status()
    
    def show_config(self, args):
        self.star_rail.show_config()
        
    def show_details(self, args):
        self.star_rail.streaming_assets()
    
    def play_time(self, args):
        self.star_rail.verbose_play_time()    
    
    # =================================================
    # ===============| LAUNCH DRIVER | ================
    # =================================================
    
    def start(self, args):
        self.star_rail.start()
        
    def stop(self, args):
        self.star_rail.terminate()
        
    def schedule(self, args):
        
        def verbose_add_usage():
            aprint(f"To schedule a new game start, run:\n{color_cmd('starrail schedule add --action start --time 10:30', True)}")
        
        def verbose_general_usage():
            headers = [Printer.to_lightpurple(title) for title in ["Example Command", "Description"]]
            data = [
                [color_cmd("schedule add --time 10:30 --action start"), "Schedule Honkai Star Rail to START at 10:30 AM"],
                [color_cmd("schedule add --time 15:30 --action stop"),  "Schedule Honkai Star Rail to STOP  at 3:30 PM"],
                [color_cmd("schedule remove"), "Remove an existing scheduled job"], 
                [color_cmd("schedule show"), "Show all scheduled jobs and their details"],
                [color_cmd("schedule clear"), "Cancel all schedule jobs (irreversible)"]
            ]
            
            tab = tabulate.tabulate(data, headers)
            print("\n" + tab + "\n")

        
        if args.subcommand == "add":
            op_type = None
            if args.action.lower().strip() == "start":
                op_type = OperationTypes.START
            elif args.action.lower().strip() == "stop":
                op_type = OperationTypes.END
            else:
                verbose_add_usage()
                return
                
            if not args.time:
                verbose_add_usage()
                return
                
            self.scheduler.add_new_schedule(args.time, op_type)
            
        elif args.subcommand == "remove":
            self.scheduler.remove_schedule()
            
        elif args.subcommand == "show":
            self.scheduler.show_schedules()
        
        elif args.subcommand == "clear":
            self.scheduler.clear_schedules()
        
        elif args.subcommand == "help":
            verbose_general_usage()

        else:
            aprint(f"{Printer.to_lightred('Error: expecting subcommand.')} See below for exmaple usage.")
            verbose_general_usage()
        
        
    # =================================================
    # =================| AUTOMATION | =================
    # =================================================
    
    def automation(self, args):
        
        def force_admin():
            if not is_admin():
                aprint(f"{Printer.to_lightred('Admin permission required for automation')}.\nWould you like to elevate the permissions to admin? [y/n] ", end="")
                if input("").strip().lower() == "y":
                    StarRailPermissionsHandler.elevate()
                    raise SRExit()
                else:
                    raise SRExit()
        
        if args.action == "record":
            force_admin()
            self.automation_controller.record_sequences()
        
        elif args.action == "run":
            force_admin()
            self.automation_controller.run_requence()

        elif args.action == "show":
            self.automation_controller.show_sequences()
            
        elif args.action == "remove":
            self.automation_controller.delete_sequence()

        elif args.action == "clear":
            self.automation_controller.clear_sequences()

        else:
            self.automation_controller.verbose_general_usage()
        
    def click_continuously(self, args):
        def force_admin(args):
            if not is_admin():
                aprint(f"{Printer.to_lightblue('Admin permission required for clicks to be registered in-game')}.\nWould you like to elevate the permissions to admin? [y/n] ", end="")
                if input("").strip().lower() == "y":
                    StarRailPermissionsHandler.elevate([
                        "click",
                        "--clicks", args.clicks,
                        "--interval", args.interval,
                        "--randomize", args.randomize,
                        "--hold", args.hold,
                        "--delay", args.delay,
                        "--quiet" if args.quiet else ""
                    ])
                    raise SRExit()
                else:
                    raise SRExit()
        
        cc_controller = ContinuousClickController()
        force_admin(args)
        cc_controller.click_continuously(args.clicks, args.interval, args.randomize, args.hold, args.delay, args.quiet)
        
    # =================================================
    # ==================| KEY URLS | ==================
    # =================================================
    
    def homepage(self, args):
        self.web_controller.homepage()
        
    def hoyolab(self, args):
        self.web_controller.hoyolab()
        
    def youtube(self, args):
        self.web_controller.youtube()
        
        
    # ===================================================
    # ===============| UTILITY FUNCTIONS | ==============
    # ===================================================

    def screenshots(self, args):
        self.star_rail.screenshots()

    def game_logs(self, args):
        self.star_rail.logs()

    def decode(self, args):
        ascii_binary_decoder = StarRailBinaryDecoder()
        ascii_binary_decoder.user_decode(args.path, args.min_length)

    def pulls(self, args):
        self.star_rail.show_pulls()

    def webcache(self, args):
        if not args.quiet:
            print_webcache_explanation()
        
        if args.announcements:
            self.star_rail.webcache_announcements()
        elif args.events:
            self.star_rail.webcache_events()
        else:
            self.star_rail.webcache_all()
            


    # =================================================
    # =============| BLOCKING FUNCTIONS | =============
    # =================================================
    
    def configure(self, args):
        
        if self.star_rail.config.full_configured():
            aprint(Printer.to_lightgreen("Configuration Already Completed!"))
            return
        
        # os.system("cls")
        
        if self.star_rail.config.disclaimer_configured() == False:
            # print(Printer.to_skyblue("\n\n - STEP 1 OF 2. DISCLAIMER AGREEMENT - \n"))
            step_two_text = " - STEP 1 OF 2. DISCLAIMER AGREEMENT - "
            print(Printer.to_skyblue(f"\n\n {'='*len(step_two_text)}"))
            print(Printer.to_skyblue(f" {step_two_text}"))
            print(Printer.to_skyblue(f" {'='*len(step_two_text)}\n"))
            print_disclaimer()
            
            print(Printer.to_lightred("[IMPORTANT] Please read the disclaimer above before continuing!"))
            if input("AGREE? [y/n] ").lower() == "y":
                self.star_rail.config.disclaimer = True
                self.star_rail.config.save_current_config()
            else:
                return
        
        if self.star_rail.config.path_configured() == False:
            step_two_text = "- STEP 2 OF 2. SET UP GAME PATH (StarRail.exe) -"
            print(Printer.to_skyblue(f"\n\n {'='*len(step_two_text)}"))
            print(Printer.to_skyblue(f" {step_two_text}"))
            print(Printer.to_skyblue(f" {'='*len(step_two_text)}\n"))
            
            logt = f"Auto Detecting Honkai: Star Rail ({Printer.to_lightgrey('this may take a while')})..."
            with Loader(logt, end=None):
                star_rail_game_detector = StarRailGameDetector()
                game_path = star_rail_game_detector.find_game()
                
                if game_path == None:
                    print(CURSOR_UP_ANSI, flush=True)
                    aprint(Printer.to_lightred("Cannot locate game Honkai: Star Rail.") + " "*15 + f"\nFile issue at '{ISSUES}' for more help.")
                    raise SRExit()

                self.star_rail.config.set_path(game_path)
                self.star_rail.config.save_current_config()

                print(CURSOR_UP_ANSI, flush=True)
                aprint("Game found at: " + game_path + " "*10)
            
        aprint("Configuration Complete!")
        

    # ===================================================
    # ===============| HELPER FUNCTIONS | ===============
    # ===================================================
    
    def elevate(self, args):
        StarRailPermissionsHandler.elevate(args.arguments)


    # =================================================
    # ===============| CLI DRIVERS | ==================
    # =================================================
    
    def print_title(self):
        
        # columns, _ = shutil.get_terminal_size(fallback=(80, 20))
        # bar = '▬' * (columns//1 - 12)
        # bar = Printer.to_lightblue(f"▷ ▷ ▷ {bar} ◁ ◁ ◁")
        # print(bar)
        
        title = Printer.to_lightblue(
r"""
 ____  _             ____       _ _    ____ _     ___ 
/ ___|| |_ __ _ _ __|  _ \ __ _(_) |  / ___| |   |_ _|
\___ \| __/ _` | '__| |_) / _` | | | | |   | |    | | 
 ___) | || (_| | |  |  _ < (_| | | | | |___| |___ | | 
|____/ \__\__,_|_|  |_| \_\__,_|_|_|  \____|_____|___|
""")
        
        desc = Printer.to_purple("""A lightweight Command Line Utility For Honkai: Star Rail!""")
        postfix = Printer.to_lightgrey(REPOSITORY)
        author = Printer.to_lightgrey(f"By {AUTHOR}")
        
        print(center_text(title))
        print_centered(f"{desc}\n{postfix}\n{author}\n")
    
    def print_init_help(self):
        access_time = colored(f"Access Time: {DatetimeHandler.get_datetime_str()}", "dark_grey")
        username = getpass.getuser()
        isadmin = "ADMIN" if is_admin() else "USER"
        
        quit_cmd = Printer.to_purple("exit")
        cls_cmd = Printer.to_purple("clear")
        help_cmd = Printer.to_purple("help")
        
        dev_str = ""
        # if DEVELOPMENT:
        #     dev_str = f"({Printer.to_lightred("Dev=True")}) {Printer.to_lightgrey("Development commands available.")}\n"
            
        welcome_str = f"Welcome to the {BASENAME} Environment ({VERSION_DESC}-{VERSION})"
        exit_str = f"Type '{quit_cmd}' to quit {SHORTNAME} CLI"
        cls_str = f"Type '{cls_cmd}' to clear terminal"
        help_str = f"Type '{help_cmd}' to display commands list"
    
        print(f"{dev_str}{welcome_str}\n  {help_str}\n  {exit_str}\n  {cls_str}\n")
    
    def clear_screen(self):
        os.system('cls')
    
    def check_custom_commands(self, user_input: str):
        # Return 0 to continue loop, 1 to short-circit loop and 'continue' loop, 2 to exit loop

        if user_input.lower() in ['exit', 'quit']:
            self.clear_screen()
            return 2
        
        if user_input.lower() in ['clear', "cls", "reset"]:
            self.clear_screen()
            self.print_title()
            
            exit_cmd = color_cmd("exit", with_quotes=True)
            print(f"Terminal cleared. Type {exit_cmd} to quit.")
            return 1
        
        if user_input.strip() == '':
            return 1
    
        return 0
    
    def setup_key_bindings(self):
        readline.parse_and_bind(r'"\C-w": backward-kill-word')
        readline.parse_and_bind(r'"\C-a": beginning-of-line')
        readline.parse_and_bind(r'"\C-e": end-of-line')
        readline.parse_and_bind(r'"\C-u": unix-line-discard')
        readline.parse_and_bind(r'"\C-k": kill-line')
        readline.parse_and_bind(r'"\C-y": yank')
        readline.parse_and_bind(r'"\C-b": backward-char')
        readline.parse_and_bind(r'"\C-f": forward-char')
        readline.parse_and_bind(r'"\C-p": previous-history')
        readline.parse_and_bind(r'"\C-n": next-history')
        readline.parse_and_bind(r'"\C-b": backward-word')
        readline.parse_and_bind(r'"\C-f": forward-word')

    def start_cli(self, parser: argparse.ArgumentParser):
        prefilled = False
        
        # =============| SET CLI MODE |==============
        constants.CLI_MODE = True
        
        # ============| SETUP READLINE |=============
        self.setup_key_bindings()

        # ==============| PRINT TITLE |==============
        self.clear_screen()
        self.print_title()
        self.print_init_help()
        
        cli_env_alert = False
        # ================| CLI LOOP |================
        while True:
            try:
                starrail_cli = colored(f"{DatetimeHandler.get_time_str()} StarRail", "dark_grey")
                print(f"[{starrail_cli}] > ", end="", flush=True)
                
                user_input = input().strip()
                continue_loop = self.check_custom_commands(user_input)
                if continue_loop == 1:
                    continue
                elif continue_loop == 2:
                    break
                
                # Verify that the stdout and stderr aren't closed
                if sys.stdout.closed or sys.stderr.closed:
                    text = "STDOUT and STDERR" if sys.stdout.closed and sys.stderr.closed \
                        else "STDOUT" if sys.stdout.closed \
                        else "STDERR"
                    aprint(f"System {text} has been closed unexpectedly. Exiting {BASENAME} environment...")
                    sys.exit()
                
                # =============| PARSE ARGUMENT |=============
                if user_input.startswith(COMMAND):
                    user_input = user_input.lstrip(COMMAND).strip() 
                    
                    if not cli_env_alert:
                        print(Printer.to_lightgrey(f"Currently in the StarRail CLI environment. You may call `{user_input}` directly without the `{COMMAND}` prefix."))
                        cli_env_alert = not cli_env_alert
                    
                args = parser.parse_args(user_input.split())
                if hasattr(args, 'func'):
                    try:
                        args.func(args)
                    except SRExit:
                        continue

                else:
                    parser.print_help()
            
        # ==============| ON EXCEPTION |==============
            except KeyboardInterrupt:
                # print("\nNote: Type 'exit' to quit.")
                print("")
                continue
            except SystemExit:
                continue
            

    # ================================================
    # ==================| FIREFLY | ==================
    # ================================================
    
    def firefly(self, args):
        lines = [
            "   I dreamed of a scorched earth.",
            "   A new shoot sprouted from the earth.",
            "   It bloomed in the morning sun",
            "   ... and whispered to me.",
            "   Like fyreflies to a flame...",
            "   life begets death.",
            "",
            "                  -- Firefly S.A.M."
        ]
        text = "\n".join(lines)
        
        firefly_colors = [
            Printer.to_pale_yellow,
            Printer.to_light_blue,
            Printer.to_teal,
            Printer.to_turquoise,
            # Printer.to_dark_teal,
            Printer.to_turquoise,
            Printer.to_teal,
            Printer.to_light_blue,
            Printer.to_pale_yellow,
        ]

        result = ""
        color_index = 0
        for char in text:
            if char != "\n":
                color_func = firefly_colors[color_index % len(firefly_colors)]
                result += color_func(char)
                color_index += 1
            else:
                result += "\n"
        print("\n" + result)
            

