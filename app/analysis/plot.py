from .format import cutCovid, getSave, formatfullCSV, add_bar_label, week_prepare
import matplotlib.pyplot as plt
import pandas as pd
import os

a_cov, b_cov = cutCovid()
a_save, b_save = getSave()
cineData = formatfullCSV()

def createYearPlot():
    semDiff_a = a_cov.groupby(['year']).Attendance.mean().sort_index()
    semDiff_b = b_cov.groupby(['year']).Attendance.mean().sort_index()

    ax = plt.gca()

    plt.bar(semDiff_b.index, semDiff_b.values, color = 'orange')
    currPos = add_bar_label(ax, semDiff_b.index, 0)

    plt.bar(semDiff_a.index, semDiff_a.values, color = 'blue')
    add_bar_label(ax, semDiff_a.index, currPos)

    ax.axes.xaxis.set_ticklabels([])
    plt.tick_params(bottom = False)

    plt.xlabel('Semester')
    plt.ylabel('Besucherzahl')
    plt.legend(['Before Covid', 'After Covid'])
    plt.title("Durchschnittliche Besucherzahlen pro Semester")
    
    plt.savefig("data/plots/SemesterPlotMean.png", dpi = 250)
    plt.clf()

def createYearPlotMedian():
    semDiff_a = a_cov.groupby(['year']).Attendance.median().sort_index()
    semDiff_b = b_cov.groupby(['year']).Attendance.median().sort_index()

    ax = plt.gca()

    plt.bar(semDiff_b.index, semDiff_b.values, color = 'orange')
    currPos = add_bar_label(ax, semDiff_b.index, 0)

    plt.bar(semDiff_a.index, semDiff_a.values, color = 'blue')
    add_bar_label(ax, semDiff_a.index, currPos)

    ax.axes.xaxis.set_ticklabels([])
    plt.tick_params(bottom = False)

    plt.xlabel('Semester')
    plt.ylabel('Besucherzahl')
    plt.legend(['Before Covid', 'After Covid'])
    plt.title("Median der Besucherzahlen pro Semester")
    
    plt.savefig("data/plots/SemesterPlotMedian.png", dpi = 250)
    plt.clf()

def createSemesterVariancePlot():
    semDiff_a = a_cov.groupby(['year']).Attendance.var().sort_index()
    semDiff_b = b_cov.groupby(['year']).Attendance.var().sort_index()

    plt.bar(semDiff_b.index, semDiff_b.values, color = 'orange')
    plt.bar(semDiff_a.index, semDiff_a.values, color = 'blue')

    plt.xticks(rotation=90)
    plt.tick_params(bottom = False)

    plt.xlabel('Semester')
    plt.ylabel('Varianz')
    plt.legend(['Before Covid', 'After Covid'])
    plt.title("Varianz der Besucherzahl pro Semester")
    
    plt.savefig("data/plots/SemesterPlotVariance.png", dpi = 250, bbox_inches = "tight")
    plt.clf()

def createRatingPlot():
    rates_a = a_save.groupby(['Rating'])['Attendance'].mean()
    rates_b = b_save.groupby(['Rating'])['Attendance'].mean()

    plt.scatter(rates_b.index, rates_b.values, color='orange')
    plt.scatter(rates_a.index, rates_a.values)
   
    plt.xlabel('Rating')
    plt.ylabel('Besucherzahl')
    plt.title("Rating (0-10) zu Besucherzahl")
    plt.legend(['Before Covid', 'After Covid'], loc = 'upper left')

    plt.savefig("data/plots/RatingPlot.png", dpi = 250)
    plt.clf()

def createAgePlots(xlim: list):
    plt.scatter(b_save['MovieAge'] / pd.to_timedelta('365 days'), b_save['Attendance'], color = 'orange')
    plt.scatter(a_save['MovieAge'] / pd.to_timedelta('365 days'), a_save['Attendance'])
    plt.xlabel('Filmalter')
    plt.xlim(xlim)
    plt.ylabel('Besucherzahl')
    plt.title("Filmalter zu Besucherzahl")
    plt.legend(['Before Covid', 'After Covid'])

    plt.savefig(f"data/plots/Age{xlim}.png", dpi = 250)
    plt.clf()


def createTypePlot():
    semType_a = a_cov.groupby(cineData['Semester'].str.split(" ").str[0])['Attendance'].mean()
    semType_b = b_cov.groupby(cineData['Semester'].str.split(" ").str[0])['Attendance'].mean()

    plt.bar(semType_b.index, semType_b.values, color = "orange")
    plt.bar(semType_a.index, semType_a.values)

    plt.legend(['Before Covid', 'After Covid'])

    plt.xlabel('Semestertype')
    plt.ylabel('Besucherzahl')
    plt.title("Durchschnittliche Besucherzahl pro Semestertyp")

    plt.savefig("data/plots/SemTypePlot.png", dpi = 250)
    plt.clf()

def createWeekdayPlot():
    week_a = week_prepare(a_cov)
    week_b = week_prepare(b_cov)

    plt.bar(week_b.index, week_b.values, color="orange")
    plt.bar(week_a.index, week_a.values)

    plt.legend(['Before Covid', 'After Covid'])

    plt.xlabel('Wochentag')
    plt.ylabel('Besucherzahl')
    plt.title("Durchschnittliche Besucherzahl pro Wochentag")

    plt.savefig("data/plots/WeekdayPlot.png", dpi = 250)
    plt.clf()

def createGenrePlot():
    genre_a, genre_b = a_cov.dropna(subset=['Genre']), b_cov.dropna(subset=['Genre'])
    genre_a = genre_a[genre_a['MovieAge'] > pd.Timedelta(days=0)]
    genre_b = genre_b[genre_b['MovieAge'] > pd.Timedelta(days=0)]
    
    genre_a['Genre'] = genre_a['Genre'].apply(lambda x: x[1:-1].replace(' ', '').split(','))
    genre_b['Genre'] = genre_b['Genre'].apply(lambda x: x[1:-1].replace(' ', '').split(','))

    g_a = genre_a.explode('Genre').groupby(['Genre'])['Attendance'].mean().sort_values()
    g_b = genre_b.explode('Genre').groupby(['Genre'])['Attendance'].mean().sort_values()

    g_b.index = g_b.index.str.replace("'", "")
    g_a.index = g_a.index.str.replace("'", "")

    ax = plt.gca()

    plt.bar(g_b.index, g_b.values, color = 'orange')
    currPos = add_bar_label(ax, g_b.index, 0)

    plt.bar(g_a.index, g_a.values, color = 'blue')
    add_bar_label(ax, g_a.index, currPos)

    ax.axes.xaxis.set_ticklabels([])
    plt.tick_params(bottom = False)

    plt.xlabel('Genre')
    plt.ylabel('Besucherzahl')
    plt.legend(['Before Covid', 'After Covid'])
    plt.title("Durchschnittliche Besucherzahl pro Genre")

    plt.savefig("data/plots/GenrePlot.png", dpi = 250)
    plt.clf()

def createPlotYear(yearPath: str):
    semester_df = pd.read_csv(yearPath)
    file_name = os.path.basename(yearPath)
    file_name = os.path.splitext(file_name)[0]
    year = file_name.split("_")[1]

    plt.bar(x=semester_df['Titel'], height=semester_df['Attendance'], color="blue")

    plt.xticks(rotation=90)
    plt.tick_params(bottom = False)

    plt.xlabel('Film', fontweight = 'bold')
    plt.ylabel('Besucherzahl', fontweight = 'bold')
    if 'winter' in yearPath:    
        plt.title(f"WiSe {year}", fontweight = 'bold')
    else:
        plt.title(f"Sose {year}", fontweight = 'bold')
    
    plt.savefig(f"data/plots/{file_name}.png", dpi = 250, bbox_inches = "tight")
    plt.clf()

def createAllPlotsPipe():
    createYearPlot()
    createYearPlotMedian()
    createSemesterVariancePlot()
    createWeekdayPlot()
    createAgePlots([0,5])
    createAgePlots([5, 50])
    createTypePlot()
    createRatingPlot()
    createGenrePlot()
