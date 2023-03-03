import winreg
import os
import concurrent.futures
import shutil
import time
import importlib.util
from git import Repo

class LazyInstall:
    '''
    For steam versions don't modify variable GAME_LOCATION
    if your installation is in different place set your location as string:
    'C:\SteamLibrary\steamapps\common\RimWorld\Mods'
    '''
    GAME_LOCATION = False
    CPU_TO_USE = int(round(((os.cpu_count() + 4) / 3),0))
    UPDATE = {'MESSAGE':"Do you want to UPDATE installed mods? [Y/N] \n", 'A': "N"}
    INSTALL = {'MESSAGE':"Do you want to INSTALL new mods from list? [Y/N] \n", 'A': "N"}
    REINSTALL = {'MESSAGE':"Do you want to DELETE incorrectly installed mods and reinstall them? [Y/N] \n", 'A': "N"}
    REPO_LIST = [
                ['rjw', 'https://gitgud.io/Ed86/rjw.git'],
                ['rjw-whoring', 'https://gitgud.io/Ed86/rjw-whoring.git'],
                ['rjw-Whorebeds', 'https://gitgud.io/Ed86/rjw-whorebeds.git'],
                ['rjw-std', 'https://gitgud.io/Ed86/rjw-std.git'],
                ['rjw-cum', 'https://gitgud.io/Ed86/rjw-cum.git'],
                ['rjw-ia', 'https://gitgud.io/Ed86/rjw-ia.git'],
                ['rjw-fb', 'https://gitgud.io/Ed86/rjw-fb.git'],
                ['rjw-fh', 'https://gitgud.io/Ed86/rjw-fh.git'],
                ['rjw-ex', 'https://gitgud.io/Ed86/rjw-ex.git'],
                ['rimworld-animations-patch', 'https://gitgud.io/AbstractConcept/rimworld-animations-patch.git'],
                ['overt-underwear', 'https://gitgud.io/AbstractConcept/overt-underwear.git'],
                ['privacy-please', 'https://gitgud.io/AbstractConcept/privacy-please.git'],
                ['Rimworld-Animations', 'https://gitgud.io/c0ffeeeeeeee/rimworld-animations.git'],
                ['rjwanimaddons-animalpatch', 'https://gitgud.io/Tory/rjwanimaddons-animalpatch.git'],
                ['rjwanimaddons-xtraanims', 'https://gitgud.io/Tory/rjwanimaddons-xtraanims.git'],
                ['animaddons-voicepatch', 'https://gitgud.io/Tory/animaddons-voicepatch.git'],
                ['rjw-toys-and-masturbation', 'https://gitgud.io/c0ffeeeeeeee/rjw-toys-and-masturbation.git'],
                ['licentia-labs', 'https://gitgud.io/John-the-Anabaptist/licentia-labs.git'],
                ['nephila-rjw', 'https://gitgud.io/HiveBro/nephila-rjw.git'],
                ['RJW_Menstruation', 'https://gitgud.io/lutepickle/rjw_menstruation.git'],
                ['s16s-extension', 'https://gitlab.com/Hazzer/s16s-extension.git'],
                ['rjw-events', 'https://gitgud.io/c0ffeeeeeeee/rjw-events.git'],
                ['scc-lewd-sculptures', 'https://gitgud.io/SpiritCookieCake/scc-lewd-sculptures.git'],
                ['rimvore-2', 'https://gitlab.com/Nabber/rimvore-2'],
                ['Rimnosis', 'https://github.com/WolfoftheWest/Rimnosis.git'],
                ['rimnude-unofficial', 'https://gitgud.io/Tory/rimnude-unofficial.git'],
                ['oty-nude-unofficial', 'https://gitgud.io/Tory/oty-nude-unofficial.git'],
                ['rjw-genes', 'https://github.com/vegapnk/rjw-genes.git'],
                ['RJW-Sexperience', 'https://github.com/amevarashi/RJW-Sexperience.git'],
                ['rjw-sexperience-ideology', 'https://gitgud.io/amevarashi/rjw-sexperience-ideology.git'],
                ['coffees-rjw-ideology-addons', 'https://gitgud.io/c0ffeeeeeeee/coffees-rjw-ideology-addons.git'],
                ['rjw-milkable-colonists-biotech', 'https://gitgud.io/Onslort/rjw-milkable-colonists-biotech.git'],
                ['rjw-milking-machine', 'https://github.com/bipassed/rjw-milking-machine.git'],

                # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                # ::Optional mods: delete "::" at beginning of line to add::
                # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

                ['rimworld-animations-patch', 'https://gitgud.io/AbstractConcept/rimworld-animations-patch.git'], # Not updated for 1.4
                ['rjw-race-support', 'https://gitgud.io/AsmodeusRex/rjw-race-support.git'], # Not the mod, only build files; you'll need to compile to get the mod itself
                ['betterrjw', 'https://gitgud.io/EaglePhntm/betterrjw.git'], # changes values in RJW; haven't tested this too much
                ['rimjobworld-ideology-addon', 'https://gitgud.io/Tittydragon/rimjobworld-ideology-addon.git'], # Work in progress; still buggy
                ['rjw-pawnmorpher-support', 'https://gitgud.io/a-flock-of-birds/rjw-pawnmorpher-support.git'], # Requires PawnMorpher
                ['DirtyTalk', 'https://github.com/Azaz3l/DirtyTalk.git'],
                ['SpeakUp', 'https://github.com/jptrrs/SpeakUp.git'], # DirtyTalk depends on SpeakUp
                ]
    
    WELCOME = ("yukiller version of Lazy Installer and Updater for RJW and Submods\n" \
               "Inspiered by C0ffees and Techno665 Lazy Installer " \
               "& Updater for RJW and Submods\n")

    def __init__(self):
        if not os.path.isdir(self.GAME_LOCATION):
            self.GameLocation()
        if not os.path.isdir(self.GAME_LOCATION):
            print(f"Check GAME_LOCATION: {self.GAME_LOCATION}")
        else:
            print(f"{self.GAME_LOCATION}")
            """ Permissions to start different functions unattended. """
            temp_s = [self.UPDATE, self.INSTALL, self.REINSTALL]
            for id_, var in enumerate(temp_s):
                if not var['A'].upper() in ('Y', 'YES'):
                    while True:
                        temp_var = input(var['MESSAGE'])
                        if temp_var.upper() in ('YES', 'Y', 'NO', 'N'):
                            #print(temp_s[id_])
                            temp_s[id_].update({'A':temp_var})
                            del temp_var
                            break
                        else:
                            continue
            self.UPDATE, self.INSTALL, self.REINSTALL = temp_s
            del temp_s

    def start(self):
        os.system('cls')
        print(self.WELCOME)

        t1 = time.perf_counter()

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.CPU_TO_USE) as executor:
            for _ in executor.map(self.MultiproccessingLoop, self.REPO_LIST):
                print(_)

        t2 = time.perf_counter()
        print(f"Finished in {round(t2-t1, 0)} seconds")
        input("Press enter to exit;")

    def GameLocation(self) -> os:
        try:
            reg_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Steam App 294100"
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
            
            game_install, regtype = winreg.QueryValueEx(registry_key, "InstallLocation")
            self.GAME_LOCATION = os.path.join(game_install, "Mods")
            del regtype, game_install
        except:
            self.GAME_LOCATION = False
        finally:
            winreg.CloseKey(registry_key)

    def MultiproccessingLoop(self,
                    var: list) -> str:
        name, link = var
        mod_loc = os.path.join(self.GAME_LOCATION, name)
        if os.path.isdir(mod_loc):
            if os.path.isdir(mod_loc + "/.git"):
                if self.UPDATE['A'].upper() in ('Y', 'YES'):
                    try:
                        repo = Repo(mod_loc) 
                        repo.remotes.origin.pull()
                        return f"{name} | Update completed"
                    except Exception as e:
                        return f"{name} | Update error | {e}"
                else:
                    return f"{name} | Update not allowed by user"
            else:
                if self.REINSTALL['A'].upper() in ("YES", "Y"):
                    try:
                        shutil.rmtree(mod_loc)
                        repo = Repo.clone_from(link, mod_loc)
                        return f"{name} | Reinstall completed"
                    except Exception as e:
                        return f"{name} | Reinstall error | {e}"
                else:
                    return f"{name} | Reinstall not allowed by user"
        else:
            if self.INSTALL['A'].upper() in ("YES", "Y"):
                try:
                    repo = Repo.clone_from(link, mod_loc)
                    return f"{name} | Install completed"
                except Exception as e:
                    return f"{name} | Install error | {e}"
            else:
                return f'{name} | Installation not allowed by user'

def GitCheck() -> bool:
    #pip install GitPython
    package_name = 'git'
    package_c = importlib.util.find_spec(package_name)
    if package_c is None:
        return False
    else:
        return True

if __name__ == '__main__':
    GC = GitCheck()

    if GC:
        l = LazyInstall()
        l.start()