import tkinter

from tkinter import *
# from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
import csv
import math
import locale

window = None

role_combo, country_combo, area_combo, compa_ratio_combo, level_combo, contract_fac_combo = None, None, None, None, None, None
sf_bench_lable, loc_fac_lable, lev_lable, com_lable, contract_fac_lable, how_lable, result_lable = None, None, None, None, None, None, None

roles_benchmark = []
roles_benchmark_dict = {}

roles = []
locale.setlocale(locale.LC_ALL, '')


def read_roles_csv(roles_csv):
    try:
        with open(roles_csv) as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            notFirstLine = False
            for row in reader:
                if (notFirstLine):
                    # roles_benchmark.append([row[0], row[-1]])
                    roles_benchmark_dict[row[0]] = row[-1]
                    roles.append(row[0])
                notFirstLine = True

    except FileNotFoundError:
        print("Sorry, " + fileName + " could not be found. ")

    return roles_benchmark


print(read_roles_csv("roles.csv"))

countries = []
areas = []
setup1 = {}
setup2 = {}
countries_areas_factors = []


def read_location_csv(location_csv):
    try:
        with open(location_csv) as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            notFirstLine = False
            for row in reader:
                if (notFirstLine):
                    countries_areas_factors.append(row)
                    setup1[row[0]] = ""
                    setup2[row[1]] = ""
                notFirstLine = True
    except FileNotFoundError:
        print("Sorry, " + fileName + " could not be found. ")


read_location_csv("location-factors.csv")


def get_filtered_countries():
    for country in setup1.keys():
        countries.append(country)
    print(countries)
    return countries


def get_filtered_areas():
    for area in setup2.keys():
        areas.append(area)
    print(len(areas))
    return areas


def get_sf_benchmark(role):
    if (roles_benchmark_dict.get(role) == None):
        print("Please, makesure you have selected valid selection from dropdown menu")
        # display message window here
    else:

        return roles_benchmark_dict.get(role)


# print(get_sf_benchmark("boom"))


def handle_invalid_combo_input_values(combo_name):
    messagebox.showwarning("Warning!", " Please, choose correct value for " + combo_name + " combo box")


def handle_clear():
    global role_combo, country_combo, area_combo, level_combo, compa_ratio_combo,result_lable, contract_fac_combo
    clear_warning = messagebox.askquestion("Warning!", "Are you sure you want to clear?")
    if clear_warning == 'yes':
        if (role_combo.current() != -1):
            role_combo.set('')
        if (country_combo.current() != -1):
            country_combo.set('')

        if (area_combo.current() != -1):
            area_combo.set('')

        if (level_combo.current() != -1):
            level_combo.set('')

        if (compa_ratio_combo.current() != -1):
            compa_ratio_combo.set('')
        if (contract_fac_combo.current() != -1):
            contract_fac_combo.set('')
        result_lable.config(text = "")
    else:
        return


def handle_quit():
    global window
    quit_warning = messagebox.askquestion("Warning!", "Are you sure you want to quit?")
    if quit_warning == 'yes':
        window.destroy()
    else:
        return


def handle_role_benchmark():
    if (role_combo.current() != -1):
        # print([role_combo.get(), roles_benchmark_dict.get(role_combo.get())])
        return roles_benchmark_dict.get(role_combo.get())
    else:
        print("Please you entered incorrect value for role")
        handle_invalid_combo_input_values("Role")


def handle_country_area():
    if (country_combo.current() != -1 and area_combo.current() != -1):
        print(country_combo.get(), area_combo.get())
        return country_combo.get(), area_combo.get()
    if (area_combo.current() == -1):
        handle_invalid_combo_input_values("Area")
    if (country_combo.current() == -1):
        handle_invalid_combo_input_values("Country")


def match_country_area(list):
    country_area_match = False
    for e in list:
        if (e[0] == handle_country_area()[0] and e[1] == handle_country_area()[1]):
            print("matched country : " + handle_country_area()[0] + "with country " + e[0])
            print("matched area: " + handle_country_area()[1] + "with country " + e[1])
            country_area_match = True
            return float(e[2]) / 100
        # else:
        #     print("Not matched country : " + handle_country_area()[0] + "with country " + e[0])
        #     print("Not matched area: " + handle_country_area()[1] + "with country " + e[1])
        #
        #     country_area_match = False

        # break;
    if (country_area_match == False):
        messagebox.showinfo("Information", "Country and Area doesn't match, Please choose " +
                            "correct values")


# def check_country_area_match():
#     global country_area_match
#     if(country_area_match == False):
#         messagebox.showinfo("Information", "Country and Area doesn't match, Please choose " +
#                             "correct values")


def handle_level():
    if (level_combo.current() != -1):
        print(level_combo.current())
        if level_combo.current() == 0:

            return .8
        elif level_combo.current() == 1:
            return 1.
        elif level_combo.current() == 2:

            return 1.2
        else:

            return 1.4
    else:
        handle_invalid_combo_input_values("Level")


def handle_compa_ratio():
    if (compa_ratio_combo.current() != -1):
        #  print(compa_ratio_combo.current())
        if compa_ratio_combo.current() == 0:

            return .85, .925
        elif compa_ratio_combo.current() == 1:
            return .925, .99
        elif compa_ratio_combo.current() == 2:
            return 1.0, 1.075
        else:
            return 1.075, 1.15
    else:
        handle_invalid_combo_input_values("Compa-Ratio")


def handle_contra_fact():
    if contract_fac_combo.current() != -1:
        print("test")
        if contract_fac_combo.current() == 0:
            return 1
        elif contract_fac_combo.current() == 1:
            return 1.17
    else:
        handle_invalid_combo_input_values("Contract factor")


def showSuccessMessage():
    messagebox.showinfo("Success!", "Annual Compensation detatils is successuly written to base_salary.csv")


data = [["Role", "Level", "Compa ratio", "Country", "Area", "Contract Factor", "SF Benchmark"]]


def write_to_csv():
    global data
    # write to the csv file
    with open("base_salary.csv", 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
    # release resouces when done
    csvFile.close()
    # display success
    showSuccessMessage()


def get_annual_compensation():
    global sf_bench_lable, loc_fac_lable, lev_lable, com_lable, contract_fac_lable, how_lable, result_lable
    global data
    try:
        dis_sf_ben = handle_role_benchmark()
        dis_loc_fac = match_country_area(countries_areas_factors)
        dis_lev = handle_level()
        dis_compa_low, dis_compa_high = handle_compa_ratio()[0], handle_compa_ratio()[1]
        dis_contract = handle_contra_fact()

        dis_result_low = math.ceil(int(dis_sf_ben) * dis_loc_fac * dis_lev * dis_compa_low * dis_contract)

        dis_result_high = math.ceil(math.ceil(int(dis_sf_ben) * dis_loc_fac * dis_lev * dis_compa_high * dis_contract))




    except:
        print("Exception happened")
    else:
        how_lable.config(text="How did we calculate your compensation?", width=60,  padding = 5)
        formated_sf_bm = locale.currency(int(dis_sf_ben), grouping=True)

        total = ttk.Label(text="SF benchmark | " + formated_sf_bm + "   x   " + "Location Factor | " + str(dis_loc_fac) + "   x   "
                          + "Level | " + str(dis_lev) + "   x   "
                          + "Compa-ratio | " + str(dis_compa_low) + " to " + str(dis_compa_high) + "   x   "
                          + 'Contract factor | ' + str(dis_contract), width=120, anchor = 'e', background = 'white')
        total.grid(row=10, column=0)

        formated_low = locale.currency(dis_result_low, grouping=True)
        formated_high = locale.currency(dis_result_high, grouping=True)

        result_lable.config(text=formated_low + " - " + formated_high ,
                            width=40, background = "#e7e7e7", anchor = "center")


        data.append(
            [role_combo.get(), compa_ratio_combo.get(), country_combo.get(), area_combo.get(), contract_fac_combo.get(),
             dis_sf_ben])
        data.append(["--", "--", "--", "--", "--", "--", "--"])
        data.append(["Annual Compensation", formated_low, " to ", formated_high])
        write_to_csv()




def ui():
    global window, style
    global role_combo, country_combo, area_combo, level_combo, compa_ratio_combo, contract_fac_combo
    global sf_bench_lable, loc_fac_lable, lev_lable, com_lable, contract_fac_lable, how_lable, result_lable

    window = tkinter.Tk()
    window.title("Base Salary Calculator")
    window.configure(background='white')



    base_sc_lable = ttk.Label(text="Base salary calculator" , width = 30, font = 20, padding = "5", anchor = "w", background = "white")


    base_sc_lable.grid(row=0)

    select_role_lable = ttk.Label(text="Select a role", font = 3, width = 60, anchor = "w", padding = "10", background = "white" )
    select_role_lable.grid(row=1, column=0)

    role_lable = tkinter.Label(text="Role",width = 54, anchor = "w", background = "white" )
    role_lable.grid(row=2, column=0)

    role_combo = ttk.Combobox(window, values=roles, width = 59, background = "white")
    role_combo.grid(row=3, column=0)

    level_lable = ttk.Label(text="Level", width = 63, anchor = "w", background = "white")
    level_lable.grid(row=4, column=0)

    level_combo = ttk.Combobox(window, values=["Junior",
                                               "Intermediate",
                                               "Senior",
                                               "Staff",
                                               "Manager"], width = 59)
    level_combo.grid(row=5, column=0)

    compa_ratio_lable = ttk.Label(text="Compa ratio", width = 63, anchor = "w", background = "white")
    compa_ratio_lable.grid(row=4, column=1)
    compa_ratio_combo = ttk.Combobox(window, values=["Learning the role",
                                                     "Growing in the role",
                                                     "Thriving in the role",
                                                     "Expert in the role"],
                                     width = 59)
    compa_ratio_combo.grid(row=5, column=1)

    annual_comp_lable = ttk.Label(text="Annual Compensation", width = 59, anchor = "center" ,background = "white")
    annual_comp_lable.grid(row=3, column=2)

    # get back to line separator
    hori_line = ttk.Separator(orient="horizontal").grid(row=4, column=2)

    result_lable = ttk.Label(text="", width = 30, background = "#e7e7e7")
    result_lable.grid(row=5, column=2)

    country_lable = ttk.Label(text="Country", width = 63, anchor = "w", background = "white")
    country_lable.grid(row=6, column=0)
    country_combo = ttk.Combobox(window, values=get_filtered_countries(), width = 59)
    country_combo.grid(row=7, column=0)

    area_lable = ttk.Label(text="Area", width = 63, anchor = "w", background = "white")
    area_lable.grid(row=6, column=1)
    area_combo = ttk.Combobox(window, values=get_filtered_areas(),width = 59)
    area_combo.grid(row=7, column=1)

    con_fc_lable = ttk.Label(text = "Contract Factor", background = 'white').grid(row=6, column = 2)
    contract_fac_combo = ttk.Combobox(window, values=["employee", "contractor"])
    contract_fac_combo.grid(row=7, column=2)

    hori_line = ttk.Separator(orient="horizontal").grid(row=8, column=2)
    how_lable = ttk.Label(text=" ", background="white")
    how_lable.grid(row=9, column=0)


    sf_bench_lable = ttk.Label(text="", background="white")

    sf_bench_lable.grid(row=10, column=0)



    loc_fac_lable = ttk.Label(text="", background="white")
    loc_fac_lable.grid(row=10, column=1)

    lev_lable = ttk.Label(text="", background="white")
    lev_lable.grid(row=10, column=2)

    com_lable = ttk.Label(text="", background="white")
    com_lable.grid(row=10, column=3)


    contract_fac_lable = ttk.Label(text="", background="white")
    contract_fac_lable.grid(row=10, column=4)

    calculate_button = ttk.Button(window, text="Calculate", command=get_annual_compensation, style="TButton")
    calculate_button.grid(row=5, column=3)
    clear_button = ttk.Button(window, text="Clear", command=handle_clear).grid(row=6, column=3)
    quit_button = ttk.Button(window, text="Quit", command=handle_quit).grid(row=7, column=3)

    mainloop()


ui()
