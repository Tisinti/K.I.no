from .format import *
import matplotlib.pyplot as plt
import pandas as pd

a_cov, b_cov = cutCovid()
a_save, b_save = getSave()
cineData = formatfullCSV()

def createYearPlot():
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
    plt.ylabel('Attendance')
    plt.legend(['Before Covid', 'After Covid'])
    plt.title("Median of Attendance")

    plt.savefig("data/plots/SemesterpPlot.png")
    plt.clf()

def createRatingPlot():
    rates_a = a_save.groupby(['Rating'])['Attendance'].mean()
    rates_b = b_save.groupby(['Rating'])['Attendance'].mean()

    plt.scatter(rates_b.index, rates_b.values, color='orange')
    plt.scatter(rates_a.index, rates_a.values)
   
    plt.xlabel('Rating')
    plt.ylabel('Attendance')
    plt.title("Rating to Attendance")
    plt.legend(['Before Covid', 'After Covid'], loc = 'upper left')

    plt.savefig("data/plots/RatingPlot.png")
    plt.clf()

def createAgePlots(xlim: list):
    plt.scatter(b_save['MovieAge'] / pd.to_timedelta('365 days'), b_save['Attendance'], color = 'orange')
    plt.scatter(a_save['MovieAge'] / pd.to_timedelta('365 days'), a_save['Attendance'])
    plt.xlabel('Movie Age')
    plt.xlim(xlim)
    plt.ylabel('Attendance')
    plt.title("Movie Age to Attendance")
    plt.legend(['Before Covid', 'After Covid'])

    plt.savefig(f"data/plots/Age{xlim}.png")
    plt.clf()


def createTypePlot():
    semType_a = a_cov.groupby(cineData['Semester'].str.split(" ").str[0])['Attendance'].mean()
    semType_b = b_cov.groupby(cineData['Semester'].str.split(" ").str[0])['Attendance'].mean()

    plt.bar(semType_b.index, semType_b.values, color = "orange")
    plt.bar(semType_a.index, semType_a.values)

    plt.legend(['Before Covid', 'After Covid'])

    plt.xlabel('Semestertype')
    plt.ylabel('Attendance')
    plt.title("Mean of each Semestertype")

    plt.savefig("data/plots/SemTypePlot.png")
    plt.clf()

def createWeekdayPlot():
    week_a = week_prepare(a_cov)
    week_b = week_prepare(b_cov)

    plt.bar(week_b.index, week_b.values, color="orange")
    plt.bar(week_a.index, week_a.values)

    plt.legend(['Before Covid', 'After Covid'])

    plt.xlabel('Weekday')
    plt.ylabel('Attendance')
    plt.title("Mean average on a Weekday")

    plt.savefig("data/plots/WeekdayPlot.png")
    plt.clf()


def createAllPlotsPipe():
    createYearPlot()
    createWeekdayPlot()
    createAgePlots([0,5])
    createAgePlots([5, 50])
    createTypePlot()
    createRatingPlot()
