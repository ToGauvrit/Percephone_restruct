"""Théo Gauvrit 09/06/2023
Main script to use the functions and classes defined in core and plots
"""
import os

import matplotlib
import numpy as np
import pandas as pd

import core as pc
import plots as p

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

plt.switch_backend("Qt5Agg")
directory = "/datas/Théo/Projects/Percephone/data/Amplitude_Detection/loop_format/"
roi_info = pd.read_excel(directory + "/FmKO_ROIs&inhibitory.xlsx")

# Heatmaps per group for each stimulation amplitude
# df_wt = {2: [], 4: [], 6: [], 8: [], 10: [], 12: []}
# df_ko = {2: [], 4: [], 6: [], 8: [], 10: [], 12: []}
# for folder in os.listdir(directory):
#     if os.path.isdir(directory + folder):
#         path = directory + folder + '/'
#         name = int(folder[9:13])
#         n_record = folder[14:16]
#         print(name)
#         roi_info["Recording number"] = roi_info["Recording number (Femtonics)"].str.split(" ", expand=True)[0]
#         row = roi_info[(roi_info["Number"] == name) & (roi_info["Recording number"] == n_record)]
#         if len(row) == 0:
#             continue
#         inhib_ids = np.array(list(list(row["Inhibitory neurons: ROIs"])[0].split(", ")))
#         recording = pc.RecordingStimulusOnly(path, inhibitory_ids=inhib_ids.astype(int))
#         print(np.unique(recording.stim_ampl))
#         print(len(recording.stim_time))
#         for stim_ampl in [2, 4, 6, 8, 10, 12]:
#             peri_stim = p.peristimulus(recording, stim_ampl, inh=False)
#             if not np.any(peri_stim):
#                 continue
#             if row["Genotype"].values == "WT":
#                 df_wt[stim_ampl].append(peri_stim)
#             if row["Genotype"].values == "KO":
#                 df_ko[stim_ampl].append(peri_stim)
# for stim_ampl in [2, 4, 6, 8, 10, 12]:
#     p.group_heat_map_per_stim(np.concatenate(df_wt[stim_ampl]),
#                               stim_ampl, filename="../output/detection/wt/exc/Heat_map_detection_EXC" + str(stim_ampl) + "_WT.png")
#     p.group_heat_map_per_stim(np.concatenate(df_ko[stim_ampl]),
#                               stim_ampl, filename="../output/detection/ko/exc/Heat_map_detection_EXC" + str(stim_ampl) + "_KO.png")


# Heatmaps per group for rewards
df_wt = []
df_ko = []
for folder in os.listdir(directory):
    if os.path.isdir(directory + folder):
        path = directory + folder + '/'
        name = int(folder[9:13])
        n_record = folder[14:16]
        print(name)
        roi_info["Recording number"] = roi_info["Recording number (Femtonics)"].str.split(" ", expand=True)[0]
        row = roi_info[(roi_info["Number"] == name) & (roi_info["Recording number"] == n_record)]
        if len(row) == 0:
            continue
        inhib_ids = np.array(list(list(row["Inhibitory neurons: ROIs"])[0].split(", ")))
        recording = pc.RecordingAmplDet(path, starting_trial=0, inhibitory_ids=inhib_ids.astype(int), sf=30.9609)
        if len(recording.reward_time) != 0:
            peri_rew = p.perireward(recording.reward_time,  recording.df_f_inh, recording.sf)
            if not np.any(peri_rew):
                continue
            if row["Genotype"].values == "WT":
                df_wt.append(peri_rew)
            if row["Genotype"].values == "KO":
                df_ko.append(peri_rew)

p.group_heat_map_per_stim(np.concatenate(df_wt),
                          "reward",
                          filename="../output/detection/wt/exc/Heat_map_detection_INH" + str("reward") + "_WT.png")
p.group_heat_map_per_stim(np.concatenate(df_ko),
                          "reward",
                          filename="../output/detection/ko/exc/Heat_map_detection_INH" + str("reward") + "_KO.png")

# Responsivity parameters
# start_time = time.time()
# directory = "/datas/Théo/Projects/Percephone/data/Amplitude_Detection/loop_format/"
# roi_info = pd.read_excel(directory + "FmKO_ROIs&inhibitory.xlsx")
# summary_resp_glob = pd.DataFrame()
# output_neurons_resp = pd.DataFrame()
# for folder in os.listdir(directory):
#     if os.path.isdir(directory + folder):
#         print(folder)
#         path = directory + folder + '/'
#         name = int(folder[9:13])
#         n_record = folder[14:16]
#         roi_info["Recording number"] = roi_info["Recording number (Femtonics)"].str.split(" ", expand=True)[0]
#         row = roi_info[(roi_info["Number"] == name) & (roi_info["Recording number"] == n_record)]
#         if len(row) == 0:
#             continue
#         inhib_ids = np.array(list(str(row["Inhibitory neurons: ROIs"].values[0]).split(", ")))
#         recording = pc.RecordingStimulusOnly(path, inhibitory_ids=inhib_ids.astype(int), sf=row["Frame Rate (Hz)"].values[0])
#         print(len(recording.stim_ampl))
#         sum_resp, neurons_resp = recording.compute_responsivity(row)
#         summary_resp_glob = pd.concat([summary_resp_glob, sum_resp])
#         output_neurons_resp = pd.concat([output_neurons_resp, neurons_resp])
# summary_resp_glob.to_csv("global_responsiveness_test.csv")
# output_neurons_resp.to_csv("neurons_resp_test.csv")
# print("--- %s seconds ---" % (time.time() - start_time))
#
# a = summary_resp_glob.groupby(["Amplitude"]).mean()
