from constants import *
import gspread
import random
import RollingCommands
import pygsheets
import math

# var mon = {};
# var moves = [];
#
# function myFunction() {
#   return test;
# }
#
# function ClearCells() {
#   var sheet = SpreadsheetApp.getActive();
#   sheet.getRange('B44:B68').clearContent();
#   sheet.getRange('B71:B75').clearContent();
#   sheet.getRange('L71:L75').clearContent();
#   sheet.getRange('B97:B104').clearContent();
# }
#
# function capitalizeFirstLetter(string) {
# 	return string.charAt(0).toUpperCase() + string.toLowerCase().slice(1);
# }
#
#
# function onOpen() {
#   var spreadsheet = SpreadsheetApp.getActive();
#   var menuItems = [
# 	{name: 'Generate by Species', functionName: 'bySpecies'}
#   ];
#   spreadsheet.addMenu('Pokemon', menuItems);
# }
#
# function bySpecies() {
#   if (getValue('D2').toUpperCase() === 'SPECIES') {
# 	var spreadsheet = SpreadsheetApp.getActive();
# 	var species = spreadsheet.getRange('D3');
# 	species.setValue(capitalizeFirstLetter(Browser.inputBox('Which Species?', Browser.Buttons.OK_CANCEL)));
# 	mon = getPokemonByName(getValue('D3').toUpperCase());
#
# 	if(mon === undefined) {
# 	  setValue('D3', 'Ping GPMatt for bug fixes');
# 	}
#
# 	generateMon();
#   } else {
# 	SpreadsheetApp.getUi().alert('This function only usable on pokemon sheets',Browser.Buttons.OK);
#   }
# }
#
# function generateMon() {
#   setValue('H3', (Browser.inputBox('What Level?', Browser.Buttons.OK_CANCEL)));
#   for (var i = 11; i<17; i++) {
# 	setValue('G'+i,0);
#   }
#
#   ClearCells();
#
#   var species = mon.name;
#
#   pickNature();
#
#   if (mon.male === -1) {
# 	setValue('B5', 'Genderless');
#   } else {
# 	setValue('B5', Math.random() <= mon.male ? 'Male' : 'Female');
#   }
#
#   var level = parseInt(getValue('H3'));
#   for (var l = 1; l<=level; l++) {
# 	moveEvolve(l);
#   }
#
#   setAbilities(level);
#
#   pickEdges(level);
#
#   moves.forEach(function(move, index){
# 	setValue('B'+(44+index), move);
#   });
#
#   var bonusStats = {
# 	"hp": 0,
# 	"atk": 0,
# 	"def": 0,
# 	"satk": 0,
# 	"sdef": 0,
# 	"spd": 0
#   };
#   var baseStats = {
# 	"bhp": parseInt(getValue('F11')),
# 	"batk": parseInt(getValue('F12')),
# 	"bdef": parseInt(getValue('F13')),
# 	"bsatk": parseInt(getValue('F14')),
# 	"bsdef": parseInt(getValue('F15')),
# 	"bspd": parseInt(getValue('F16'))
#   };
#
#   var levelUpPoints = parseInt(getValue('G17'));
#   for (var i = 0; i < levelUpPoints; i++) {
# 	bonusStats = setStats(bonusStats, baseStats);
#   }
#
#   setValue('G11',bonusStats['hp']);
#   setValue('G12',bonusStats['atk']);
#   setValue('G13',bonusStats['def']);
#   setValue('G14',bonusStats['satk']);
#   setValue('G15',bonusStats['sdef']);
#   setValue('G16',bonusStats['spd']);
#
#   var xp = xpneeded[level-1];
#   setValue('I3', xp);
#
# 	SpreadsheetApp.getActive().renameActiveSheet(getValue('D3'));
# }
#
# function setAbilities(level) {
#   var ability = mon.abilities[Math.floor(Math.random() * mon.abilities.length)];
#   var advability = mon.advabilities[Math.floor(Math.random() * mon.advabilities.length)];
#   var highability = pickGenderedElement(mon.highabilities);
#
#   setValue('B71', ability);
#   if (level >= 20) {
# 	setValue('B72', advability);
#   }
#   if (level >= 40) {
# 	setValue('B73', highability);
#   }
# }
#
# function pickGenderedElement(arr) {
#   var gender = getValue('B5');
#
#   if(gender === 'Male') {
# 	arr = removeArrayElementsContaining(arr, '(Female)');
# 	arr = replaceInAllStringsInArray(arr, '(Male)');
#   } else if (gender === 'Female') {
# 	arr = removeArrayElementsContaining(arr, '(Male)');
# 	arr = replaceInAllStringsInArray(arr, '(Female)');
#   }
#
#   return arr[Math.floor(Math.random() * arr.length)];
# }
#
# function replaceInAllStringsInArray(arr, str) {
#   for(var i = 0; i < arr.length; i++) {
# 	arr[i] = arr[i].replace(str,'');
#   }
#   return arr;
# }
#
# function removeArrayElementsContaining(arr, str) {
#   var result = [];
#
#   for(var i = 0; i < arr.length; i++) {
# 	if(arr[i].indexOf(str)===-1) {
# 	  result.push(arr[i]);
# 	}
#   }
#   return result;
# }
#
# function moveEvolve(level) {
#   if (mon.evolutions[level] !== undefined && getValue('K3')) {
# 	var evo = getEvolution(level);
# 	setValue('D3', capitalizeFirstLetter(evo.toLowerCase()));
#
# 	mon = getPokemonByName(evo);
#   }
#   for (var m in mon.moves) {
# 	var move = mon.moves[m].split(' ');
# 	if (move[0] == level) {
# 	  move.shift();
# 	  move = move.join(' ');
# 	  if (moves.length < 25) {
# 		moves.push(move);
# 	  } else if (Math.random() > 0.5) {
# 		moves[Math.floor(Math.random() * 12)] = move;
# 	  }
# 	}
#   }
# }
#
# function getEvolution(level){
#   var evo = mon.evolutions[level];
#
#   if(Array.isArray(evo)) {
# 	return pickGenderedElement(evo);
#   } else {
# 	return evo;
#   }
# }
#
# function getPokemonByName(name) {
#   for(var poke in allpokemon) {
# 	if(allpokemon[poke].name === name) {
# 	  return allpokemon[poke];
# 	}
#   }
# }
#
# function setStats(bonusStats, baseStats) {
#   var valid = getValid(bonusStats, baseStats);
#   var raisable = [];
#   valid.forEach(function (vstat) {
# 	var weight = Math.ceil(Math.sqrt(baseStats['b'+vstat]) * 10);
# 	while (weight > 0) {
# 	  raisable.push(vstat);
# 	  weight--;
# 	}
#   });
#
#   var raise;
#   raise = raisable[Math.floor(Math.random() * raisable.length)];
#   bonusStats[raise]++;
#
#   return bonusStats;
# }
#
# function pickNature() {
#   var spreadsheet = SpreadsheetApp.getActive();
#   var nature = spreadsheet.getRange('D5');
#   nature.setValue(natures[Math.floor(Math.random() * natures.length)]);
# }
#
# function pickEdges(level) {
#   var spreadsheet = SpreadsheetApp.getActive();
#   var edge1 = spreadsheet.getRange('B97');
#   var edge2 = spreadsheet.getRange('B98');
#   var edge3 = spreadsheet.getRange('B99');
#   var edge4 = spreadsheet.getRange('B100');
#   var edge5 = spreadsheet.getRange('B101');
#   var edge6 = spreadsheet.getRange('B102');
#   var edge7 = spreadsheet.getRange('B103');
#   var edge8 = spreadsheet.getRange('B104');
#   if (level >= 10) {
#   edge1.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 20) {
#   edge2.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 30) {
#   edge3.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 40) {
#   edge4.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 50) {
#   edge5.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 60) {
#   edge6.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 70) {
#   edge7.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
#   if (level >= 80) {
#   edge8.setValue(edges[Math.floor(Math.random() * edges.length)]);
#   }
# }
#
# function getValid(bonusStats, baseStats) {
#   var valid = [];
#   for (var stat in bonusStats) {
# 	var good = true;
# 	for (var ostat in bonusStats) {
# 	  if (baseStats['b'+stat] < baseStats['b'+ostat]
# 		  && parseInt(bonusStats[stat])+parseInt(baseStats['b'+stat])+1 >= parseInt(bonusStats[ostat])+parseInt(baseStats['b'+ostat])) {
# 		good = false
# 	  }
# 	}
# 	if (good) {
# 	  valid.push(stat);
# 	}
#   }
#   return valid;
# }
#
# function getValue(cell) {
#   return SpreadsheetApp.getActive().getRange(cell).getValue();
# }
#
# function setValue(cell, value) {
#   SpreadsheetApp.getActive().getRange(cell).setValue(value);
# }
#
# //For debugging
# function debugClear(){
#   setValue('Q18','');
# }
#
# //For debugging
# function debugOut(str){
#   setValue('Q18', getValue('Q18') + '\n' + str);
# }
#
# var xpneeded = [0,      10,     20,     30,     40,     50,     60,     70,     80,     90,     //1-10 110,    135,
# 160,    190,    220,    250,    285,    320,    360,    400,    //11-20 460,    530,    600,    670,    745,
# 820,    900,    990,    1075,   1165,   //21-30 1260,   1355,   1455,   1555,   1660,   1770,   1880,   1995,
# 2110,   2230,   //31-40 2355,   2480,   2610,   2740,   2875,   3015,   3155,   3300,   3445,   3645,
# //41-50 3850,   4060,   4270,   4485,   4705,   4930,   5160,   5390,   5625,   5865,   //51-60 6110,   6360,
# 6610,   6865,   7125,   7390,   7660,   7925,   8205,   8485,   //61-70 8770,   9060,   9350,   9645,   9945,
# 10250,  10560,  10870,  11185,  11505,  //71-80 11910,  12320,  12735,  13155,  13580,  14010,  14445,  14885,
# 15330,  15780,  //81-90 16235,  16695,  17160,  17630,  18105,  18585,  19070,  19560,  20055,  20555]; //91-100
# var natures = ['Cuddly','Distracted','Proud','Decisive','Patient','Desperate','Lonely','Adamant', 'Naughty',
# 'Brave','Stark','Bold','Impish','Lax','Curious','Modest','Mild','Rash', 'Quiet','Dreamy','Calm','Gentle','Careful',
# 'Sassy','Skittish','Timid','Hasty', 'Jolly','Naive','Composed','Hardy','Docile','Bashful','Quirky','Serious']; var
# edges = ['Skill Improvement (Acrobatics)','Skill Improvement (Athletics)','Skill Improvement (Combat)',
# 'Skill Improvement (Focus)', 'Skill Improvement (Perception)','Skill Improvement (Stealth)','Skill Improvement (Gen
# Edu)','Skill Improvement (Med Edu)', 'Skill Improvement (Occult Edu)','Skill Improvement (Poké Edu)',
# 'Skill Improvement (Tech Edu)', 'Skill Improvement (Survival)', 'Skill Improvement (Charm)','Skill Improvement (
# Command)','Skill Improvement (Guile)','Skill Improvement (Intimidate)','Skill Improvement (Intuition)'];


credentials = {
    "type": "service_account",
    "project_id": "undaunteddiscordbot",
    "private_key_id": "b815b93c7e0bba1070d4a2c875e4994f02d43f39",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4eHKbjM5qeK4k\n7Wu18aGFM/QQ7HjSKNk3/qpGgA0cdPVM6iSTD/Eew+/WkttRrWn211NjLDkq86GX\nemTOeTuajoUcuitWRwOR19N79qL66RZUBZoGnlA1z/3pQfX8mrxhn7KFVBOA66fy\nArf+UoKoKZQ2Qe8G8LIQxfM+ZT9zF5k1KfmKR6bvqB38L3MRMSPStSxbFzylkwJH\n9Czq+LNnIyYmyfB0qPBYwMlEDT2aPi7hzWXku9iX2qQwua0+lYOSeVyPeFfm3JJX\nwP+/iON4DU3Qq+5BBe67shoz2CbGtDphF3fHX0i6gxWv7fvaYta0xyGYXMVdYD1W\n8sftBDKPAgMBAAECggEAF0siUbEEiZ5GgyQ1wypJVowaaB6sHQGKeE8gijl2Ll84\ncGdqieVr8ZIVUXeG2Tf4FvLWtUGq0FkmUP3kB8x4McqIVXnOqhzafwqNSmx45Q0U\nxDRW4DoSb9EdQ1yQZr7VRdCIFtzof5GCSgV83VDm7bweWoGV4L75BTQxxHG9gtdD\nJJ5BAwkGLblR5j9gqU1jYLhMN/WjK8BIyBrfAvIHANjv4rLK+jjj4Ut5h4CxsxpW\n/Aqwti7T0NwiCLERhbIENkNxbFd7hr4q+yjoCW23LCUbjnx1XdiIlJuKbty8iQsu\nBYNKXvolEHv8FEzKdSSz9Nvi4esl6Hm9Dg7pBiJuRQKBgQD4Gd1L21w3q49kdh16\no0j4GKtzy2dxxVbNi3OMcUYbvX3TwUees0iG+WBcX2I9TRTzsDUbRW4oZftGJ88s\nriTwO1aV2CzDTMBgnalkqVjP9c6/RlRgpHsjB8K2ujqIkTxeH+vbQzzO4Fj98ff3\nl+PGttktlxEkdKy/Roek8T/uqwKBgQC+V/czrvMRom6Ugh4RltEGrdgicVgemqYk\nDO2LVlKWlXZ2zW26FQcxXA5AuB13/nZFd7vfvzIoC6OK/QS6a10DITJIwbE0ex9/\nUQK0DlqAAEN8EcoAJzm32pmHMTE90rvGhFnQ4VsZw9vnQjIBqcw52DmYsSCSpO8m\nJ29bUGu7rQKBgBADa1soD22wbxLm5MQzodQRk49nw4d+WzntFEouTX4g3uw5/2to\n2veLRQLxTR/zx7Rq3SKjepa07mD61M5ndw7iZZZKW6lHXOtfgb1ziL3zeaKy4WNT\nencqWxD8OCb0aNcSbGC8mEIqDNRnN8ANV7BNwPrGU17tAPFflgW5ZIz9AoGAbsIT\nB1D7Abzp6aKZSpTexqssBEa+BvjoSjv3kcfGQPdxuompGsmXqOIvLPu1shgwzBVz\nDixcTC8RmBPIx40nz2VmtC15JteqKVSDZTCg+rCslCppx5MLo+8gvSkjxRy1xTtI\nZCJt910fvb6oCI28V8B5K1+OW6Z7vlDeHF18gvUCgYBJZ0B6zhIdGyCBQ+I4gDxh\n1FfviL35Wz0qJxHnyEAnjm4X33p6jDzNyVrwr6lJyL3ixFm77y7Qes6asF9s61UF\n51GJrjLRCcC+9X1WSmB1rGM+W76SUXKBxrwj0mNe922rm+lgJPRAx7jkjVvAeRMe\nkFtJXHo5iVWUSEVV5MW6lw==\n-----END PRIVATE KEY-----\n",
    "client_email": "undaunted@undaunteddiscordbot.iam.gserviceaccount.com",
    "client_id": "112647756200358490521",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/undaunted%40undaunteddiscordbot.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)
pg = pygsheets.authorize(service_file='UndauntedBot/service_account_credentials.json')
edges_sheet = gc.open("Data Get Test Sheet")
edges = edges_sheet.worksheet("Tutoring/Breeding").get_values('PokeEdges')
sh = gc.open("Bot Auto Statter")
template = sh.worksheet("Template")
statter = None

known_moves = []
mon = None


# write command so that it sends in the mon's name with the first letter capitalized

def clear_cells():
    statter.batch_clear(['B44:B68', 'B71:B75', 'L71:L75', 'B97:B104', 'D11:D16', 'J11:J16', 'H87:K94'])


def get_gender():
    if mon.male == -1:
        return 'Genderless'
    else:
        return 'Male' if random.random() < mon.male else 'Female'


def move_evolve(level):
    global mon
    if mon.evolution[level] is not None and statter.cell('K3').value:
        statter.update('D3', mon.evolution[level].title())
        mon = mon.evolution[level]
        if isinstance(mon.evolution, list):
            mon = pick_gender(mon)

    def condition(x, lvl):
        return '{0} '.format(lvl) in x

    output = [" ".join(element.split()[1:]) for idx, element in enumerate(mon.moves) if condition(element, level)]
    global known_moves
    known_moves += output


def pick_gender(arr):
    gender = statter.cell('B5').value
    choice = next(op for op in arr if gender in op)  # op stands for option
    choice.replace('(' + gender + ')', '')
    return choice


def pick_edges(level):
    lvl = int(level)
    temp_list = edges
    if lvl < 30:
        temp_list.remove('Attack Specialty')
    temp_list.remove('Realized Potential')
    if level >= 10:
        statter.update('B97', random.shuffle(temp_list)[-1])
        temp_list.pop()
    if level >= 30:
        statter.update('B98', random.shuffle(temp_list)[-1])
        temp_list.pop()
    if level >= 50:
        statter.update('B99', random.shuffle(temp_list)[-1])
        temp_list.pop()
    if level >= 60:
        statter.update('B100', random.shuffle(temp_list)[-1])
        temp_list.pop()
    if level >= 70:
        statter.update('B101', random.shuffle(temp_list)[-1])
        temp_list.pop()
    if level >= 80:
        statter.update('B102', random.shuffle(temp_list)[-1])
        temp_list.pop()


def set_abilities(level):
    ability = mon.abilities[random.randint(0, len(mon.abilties) - 1)]
    adv_ab = mon.abilities[random.randint(0, len(mon.abilties) - 1)]
    high_ab = mon.abilities[0]
    statter.update('B71', ability)
    if int(level) >= 20:
        statter.update('B72', adv_ab)
        if int(level) >= 40:
            statter.update('B73', high_ab)


def get_valid(bonus, base):
    valid = []
    for stat in bonus:
        good = True
        for ostat in bonus:
            if base['b' + stat] < base['b' + ostat] and \
                    bonus[stat] + base['b' + stat] + 1 >= bonus[ostat] + base['b' + ostat]:
                good = False
        if good:
            valid.append(stat)
    return valid


def set_stats(bonus, base):
    valid = get_valid(bonus, base)
    raisable = []
    for stat in valid:
        weight = math.sqrt(base['b' + stat] * 10)
        while weight > 0:
            raisable.append(stat)
            weight -= 1
    increase = raisable[random.randrange(0, len(raisable))]
    bonus[increase] += 1
    return bonus


def generate_mon(mon_name, level):
    statter.update('D3', mon_name)
    statter.update('H3', level)
    statter.update_cells('G11:G16', 0)
    clear_cells()
    global mon
    mon = next(pokemon for pokemon in ALLPOKEMON if pokemon['name'] is mon_name.upper())
    statter.update('D5', RollingCommands.nature())
    statter.update('B5', get_gender())
    for i in range(int(level)):
        move_evolve(i)
    set_abilities(level)
    pick_edges(level)
    end_range = 'B' + str(43 + len(known_moves))
    statter.batch_update('B44:' + end_range, known_moves)
    bonus_stats = {
        "hp": 0,
        "atk": 0,
        "def": 0,
        "satk": 0,
        "sdef": 0,
        "spd": 0
    }
    base_stats = {
        "bhp": int(statter.cell('F11').value),
        "batk": int(statter.cell('F12').value),
        "bdef": int(statter.cell('F13').value),
        "bsatk": int(statter.cell('F14').value),
        "bsdef": int(statter.cell('F15').value),
        "bspd": int(statter.cell('F16').value)
    }
    lvl_points = statter.cell('G17').value
    for i in range(int(lvl_points)):
        bonus_stats = set_stats(bonus_stats, base_stats)

    xp = XP_VALS[int(level) - 1]
    statter.update('I3', xp)


def autostat(mon_name, level, email=None, link=None):
    new_sheet = gc.copy('1M3O95FW3KRT1pOBUNfqQ2Yk1YcrogZgLDFkkwuGxL_M', 'Temp AutoStatter',
                        folder_id='11qO1Py6VJbBFdTSy3uCTJWoheLT4cDn2')
    global statter
    if link is None and email is not None:
        statter = gc.open_by_key(new_sheet.id).get_worksheet("Template")
        generate_mon(mon_name, level)
        statter.update_title(mon_name + " " + str(statter.index))
        statted_sheet = gc.copy(new_sheet.id, 'Statted Mons (Keep this Link)',
                                folder_id='11qO1Py6VJbBFdTSy3uCTJWoheLT4cDn2')
        gc.del_spreadsheet(new_sheet.id)
        statted_sheet.share(email, perm_type='user', role='writer')
        return "https://docs.google.com/spreadsheets/d/%s" % statted_sheet.id
    elif link is not None and email is None:
        origin = gc.open_by_url(link)
        duplicate_sheet = statter.worksheet('Duplicate Me!')
        duplicate_sheet.duplicate(new_sheet_name='Template')
        statter = origin.worksheet("Template")
        generate_mon(mon_name, level)
        statter.update_title(mon_name + " " + str(statter.index))
        return link
    else:
        return "Error!"




