import argparse
from starrail.utils.utils import *

class HelpFormatHandler:
    def print_help(self, args, parser):
        for group in parser.groups:
            
            if group['description']:
                title = Printer.to_lightred(u"\u2606 " + group['title'])
                description = Printer.to_lightgrey(" : " + group['description'])
                print(f"\n{title}{description}")
            else:   
                title = Printer.to_lightred(u"\u2606 " + group['title'])
                print(f"\n{title}")
                
            for subparser in group['parsers']:
                prog_cmd = Printer.to_lightblue(subparser.prog)
                print(f"  {prog_cmd}: {subparser.description or 'No description available.'}")
                for action in subparser._actions:
                    if action.option_strings:
                        print(f"    {Printer.to_purple(', '.join(action.option_strings))}: {Printer.to_lightgrey(action.help)}")
                    else:
                        print(f"    {Printer.to_purple(action.dest)}: {Printer.to_lightgrey(action.help)}")
                print("")