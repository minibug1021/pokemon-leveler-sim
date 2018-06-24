from random import choice
from itertools import chain
import random, json, math

route_one = [{'Caterpie':10,'Metapod':10,'Ledyba':10,'Bonsly':15,'Munchlax':5,'Pikipek':20,'Yungoos':30},{'Caterpie':10,'Metapod':10,'Rattata':30,'Spinarak':10,'Bonsly':15,'Munchlax':5,'Pikipek':20}]
base_exp = {'Caterpie':39,'Metapod':72,'Ledyba':53,'Bonsly':58,'Munchlax':78,'Pikipek':53,'Yungoos':51,'Rattata':51,'Spinarak':50}

lucky_egg = 1.5
affection = 1.2
trade_status = 1.5
pokemon = 'Magby'
level = 10
xp_gained = 0
route_sel = route_one
xp_share = 1
global killed
killed = {}


def exp(base,lucky_egg,affection,enemy_level,victor_level,trade_status,able_to_evolve,xp_share):
	'''Base Exp, Lucky Egg(1.5,1), Affection(1.2,1), Enemy Level, Victor Level, Trade Status(1,1.5,1.7), Able to Evolve(1.2,1), XP Share (1,2)'''
	three = trade_status * lucky_egg * affection * able_to_evolve
	one = math.floor((1 * base * enemy_level)/(5 * xp_share))
	two_one = ((2 * enemy_level) + 10)**2.5
	two_two = (enemy_level + victor_level + 10)**2.5
	two = two_one / two_two
	final = (one * two + 1) * three
	return(math.floor(final))
	
def random_poke(route):
        #day_or_night = random.choice(route)
        day = route[0]
        return(choice(list(chain(*([k] * v for k, v in day.items())))))
	
def evolve_levels_check(pokemon):
	with open(r"C:\Users\minibug\Desktop\python stuff\evolve_levels.json",'r',encoding='utf-8') as f:
		data = json.load(f)
	try:
		if data[pokemon] > level:
			return(1)
		else:
			return(1.2)
	except:
		return(1)
		
def rate_check(pokemon):
	with open(r"C:\Users\minibug\Desktop\python stuff\exp_groups.json",'r',encoding='utf-8') as f:
		data = json.load(f)
	return(data[pokemon])
		
def earned_exp(victor_level):
	poke = random_poke(route_sel)
	try:
		killed[poke]+=1
	except:
		killed[poke] = 1
	return(exp(base_exp[poke],lucky_egg,affection,random.choice([10,11,12,13]),victor_level,trade_status,evolve_levels_check(pokemon),xp_share))

def exp_at_level(rate,level):
	if rate == 'Erratic':
		return(erratic(level))
	elif rate == 'Fast':
		return(fast(level))
	elif rate == 'Medium Fast':
		return(medium_fast(level))
	elif rate == 'Medium Slow':
		return(medium_slow(level))
	elif rate == 'Slow':
		return(slow(level))
	elif rate == 'Fluctuating':
		return(fluctuating(level))
		
def to_next_level(level):
	return(exp_at_level(rate_check(pokemon),level+1)-exp_at_level(rate_check(pokemon),level))
	
def erratic(n):
	if n <= 50:
		return(math.floor(((n**3)*(100-n))/50))
	elif 50 <= n <= 68:
		return(math.floor(((n**3)*(150-n))/100))
	elif 68 <= n <= 98:
		a = (1911 - (10*n))/3
		return(math.floor(((n**3)*a))/500)
	else:
		return(math.floor(((n**3)*(160-n))/100))
		
def fast(n):
	return(math.floor((4*n**3)/5))
	
def medium_fast(n):
	return(math.floor(n**3))
	
def medium_slow(n):
	one = (6/5)*n**3
	two = 15*n**2
	three = 100*n
	return(math.floor(one-two+three-140))
	
def slow(n):
	return(math.floor((5*n**3)/4))
	
def fluctuating(n):
	if n <= 15:
		return(math.floor((n**3)*((math.floor((n+1)/3)+24)/50)))
	elif 15 <= n <= 36:
		return(math.floor((n**3)*((n+14)/50)))
	else:
		return(math.floor((n**3)*(((math.floor(n/2)+32)/50))))
		
def grind():
        while level != 100:
                xp_gained += earned_exp(level)
                while xp_gained > to_next_level(level):
                        xp_gained -= to_next_level(level)
                        level+=1
                        print(level)
        x = ['{}\t{}\n'.format(key, killed[key]) for key in killed]
        print(''.join(x))
        a = 0
        for key in killed:
                a+=killed[key]
