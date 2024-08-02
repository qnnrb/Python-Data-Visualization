import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from pybaseball import schedule_and_record
from pybaseball import standings
from pybaseball import cache

cache.enable()

##############################################################
# Enter an MLB division name and year (after 1969) 
# to display a graph showing the game by game 
# GB (games behind) for each team in the division.
##############################################################

class Team:
    def __init__(self, full_name, name, color):
        self.full_name = full_name
        self.name = name
        self.color = color


################################################################
# Division data
# --------------
# Full and abbreviated name of each team in the division as well
# as a color to represent them on the graph.
# Every division from the 1969 season to current day is 
# represented.
#
################################################################

al_east_1999 = []
al_east_1999 += [Team(full_name, name, color) for full_name, name, color in [('Boston Red Sox', 'BOS', 'red'), ('New York Yankees', 'NYY', 'navy'), ('Toronto Blue Jays', 'TOR', 'blue'), ('Tampa Bay Rays', 'TB', 'cornflowerblue'), ('Baltimore Orioles', 'BAL', 'orange')]]

al_east_1994 = []
al_east_1994 += [Team(full_name, name, color) for full_name, name, color in [('Boston Red Sox', 'BOS', 'red'), ('New York Yankees', 'NYY', 'navy'), ('Toronto Blue Jays', 'TOR', 'blue'), ('Detroit Tigers', 'DET', 'darkblue'), ('Baltimore Orioles', 'BAL', 'orange')]]

al_east_1977 = []
al_east_1977 += [Team(full_name, name, color) for full_name, name, color in [('Boston Red Sox', 'BOS', 'red'), ('New York Yankees', 'NYY', 'navy'), ('Toronto Blue Jays', 'TOR', 'blue'), ('Detroit Tigers', 'DET', 'darkblue'), ('Baltimore Orioles', 'BAL', 'orange'), ('Milwaukee Brewers', 'MIL', 'gold'), ('Cleveland Indians', 'CLE', 'darkred')]]

al_east_1972 = []
al_east_1972 += [Team(full_name, name, color) for full_name, name, color in [('Boston Red Sox', 'BOS', 'red'), ('New York Yankees', 'NYY', 'navy'), ('Detroit Tigers', 'DET', 'darkblue'), ('Baltimore Orioles', 'BAL', 'orange'), ('Milwaukee Brewers', 'MIL', 'gold'), ('Cleveland Indians', 'CLE', 'blue')]]

al_east_1969 = []
al_east_1969 += [Team(full_name, name, color) for full_name, name, color in [('Boston Red Sox', 'BOS', 'red'), ('New York Yankees', 'NYY', 'navy'), ('Detroit Tigers', 'DET', 'darkblue'), ('Baltimore Orioles', 'BAL', 'orange'), ('Washington Senators', 'WAS', 'tomato'), ('Cleveland Indians', 'CLE', 'blue')]]

al_cen_1994 = []
al_cen_1994 += [Team(full_name, name, color) for full_name, name, color in [('Cleveland Guardians', 'CLE', 'r'), ('Chicago White Sox', 'CSW', 'black'), ('Minnesota Twins', 'MIN', 'firebrick'), ('Detroit Tigers', 'DET', 'darkblue'), ('Kansas City Royals', 'KC', 'royalblue')]]
al_west_2013 = []
al_west_2013 += [Team(full_name, name, color) for full_name, name, color in [('Oakland Athletics', 'OAK', 'forestgreen'), ('Los Angeles Angels', 'LAA', 'red'), ('Texas Rangers', 'TEX', 'dodgerblue'), ('Houston Astros', 'HOU', 'darkorange'), ('Seattle Mariners', 'SEA', 'mediumturquoise')]]

nl_east = []
nl_cen = []
nl_west = []

def get_team_data(division_name, year):
    division_data = np.empty([5, 161])
    index = 0
    division = []
    name_and_colors = [[0 for i in range(2)] for j in range(5)]

    if division_name == "AL East":
        if int(year) > 1998:
            division = al_east_1999
        elif int(year) > 1993:
            division = al_east_1994
    
    elif division_name == "AL Central" and int(year) > 1993:
        division = al_cen_1994
    elif division_name == "AL West" and int(year) > 2012:
        division = al_west_2013

    for team in division:
        print(type(year))
        team_data = schedule_and_record(int(year), team.name)
        team_gb = team_data["GB"].values[1:162]
        team_gb[team_gb == 'Tied'] = 0

        for game in range(len(team_gb)):
            game_str = str(team_gb[game])
            if (game_str[0:2] == 'up'):
                team_gb[game] = float(game_str[2:])

            else:
                team_gb[game] = -abs(float(team_gb[game]))
            
        division_data[index] = team_gb
        name_and_colors[index][0] = team.full_name
        name_and_colors[index][1] = team.color
        index += 1
    
    return division_data, name_and_colors

        

def main():
    plt.style.use('fivethirtyeight')
    x = []
    y, y1, y2, y3, y4 = ([] for i in range(5))

    print("Enter division name: ")
    division_name = input()
    print("Enter year: ")
    year = input()

    team_gb_data, team_info = get_team_data(division_name, year)

    fig, ax = plt.subplots()
    ax.set_title("AL West Standings Day by Day")
    ax.set_xlabel("Game #")
    ax.set_ylabel("Games Behind")

    def animate(frame):
        x.append(frame)

        ax.clear()
        y.append(team_gb_data[0][frame])
        ax.step(x, y, color=team_info[0][1], label=team_info[0][0])

        y1.append(team_gb_data[1][frame])
        ax.step(x, y1, color=team_info[1][1], label=team_info[1][0])

        y2.append(team_gb_data[2][frame])
        ax.step(x, y2, color=team_info[2][1], label=team_info[2][0])

        y3.append(team_gb_data[3][frame])
        ax.step(x, y3, color=team_info[3][1], label=team_info[3][0])

        y4.append(team_gb_data[4][frame])
        ax.step(x, y4, color=team_info[4][1], label=team_info[4][0])

        ax.set_xlim([0, 161])
        ax.set_ylim([-50, 25])
    
    ani = animation.FuncAnimation(fig, animate, frames = 161, interval = 200)

    fig.legend()
    plt.show()

if __name__ == "__main__":
    main()