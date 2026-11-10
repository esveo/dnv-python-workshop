"""Check report for a grid (starting code of exercise 06).

A script in the style of a PowerFactory script that has grown over time:
one long sequence, limits as numbers in the code, output and domain logic mixed.

Usage: uv run python exercises/06/grid_check.py
"""

from datetime import datetime

from grid_analysis import powerfactory_fake as powerfactory


def create_check_report():
    app = powerfactory.GetApplication()
    app.ActivateProject("North Grid Peak Load")

    ldf = app.GetFromStudyCase("ComLdf")
    ldf.Execute()

    rows = []
    rows.append("Check report of " + datetime.now().strftime("%d.%m.%Y %H:%M"))
    rows.append("")

    count = 0
    for node in app.GetCalcRelevantObjects("*.ElmTerm"):
        u = node.GetAttribute("m:u")
        if u < 0.95:
            rows.append(f"{node.loc_name}: undervoltage ({u:.3f} p.u.)")
            count = count + 1
        elif u > 1.05:
            rows.append(f"{node.loc_name}: overvoltage ({u:.3f} p.u.)")
            count = count + 1

    for line in app.GetCalcRelevantObjects("*.ElmLne"):
        a = line.GetAttribute("c:loading")
        if a >= 100:
            rows.append(f"{line.loc_name}: overloaded ({a:.1f} %)")
            count = count + 1

    rows.append("")
    rows.append(f"{count} violations")

    with open("check_report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(rows))

    app.PrintPlain("Report written: check_report.txt")


if __name__ == "__main__":
    create_check_report()
