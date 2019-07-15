#!/usr/bin/python3
import os
import tkinter as tk
from PIL import Image

# Scale factor for image (reduce for smaller screens)
scale_factor = 0.2


def correlationTarget1Callback():
    print("Correlation target 1 selected, running...")
    os.system("python3 correlation_chain_A.py")
    return


def correlationTarget2Callback():
    print("Correlation target 2 selected, running...")
    os.system("python3 correlation_chain_B.py")
    return


def correlationTarget3Callback():
    print("Correlation target 3 selected, running...")
    os.system("python3 correlation_chain_C.py")
    return


def exitCallback():
    main_window.destroy()
    return


def updateTargetImage(a, panel):
    panel.configure(image=a)
    return


if __name__ == "__main__":
    # --- Create window ---
    main_window = tk.Tk()
    main_window.winfo_toplevel().title("HMC FWI interactive")

    # --- Target model visualization ---
    images = []

    # Load image and rescale.
    for i in range(3):
        im_temp = Image.open("data/Targets/Target%i.png" % (i + 1))
        width, height = im_temp.size
        im_temp = im_temp.resize(
            (int(width * scale_factor), int(height * scale_factor)),
            Image.ANTIALIAS,
        )
        im_temp.save("data/Targets/Target%i.ppm" % (i + 1), "ppm")
        images.append(
            tk.PhotoImage(file="data/Targets/Target%i.ppm" % (i + 1))
        )

    imagePanel = tk.Label(main_window, image=images[0])
    imagePanel.grid(row=1, column=0, columnspan=6)

    # --- Radio buttons for target model selection ---
    visualize_target = tk.IntVar()
    visualize_target.set(1)
    frame_selection = tk.LabelFrame(main_window, text="Visualize target model")
    frame_selection.grid(row=0, column=1, padx=0, pady=5, columnspan=1)
    radio = []
    radio.append(
        tk.Radiobutton(
            frame_selection,
            text="Target 1",
            variable=visualize_target,
            value=1,
            command=lambda: updateTargetImage(images[0], imagePanel),
        )
    )
    radio.append(
        tk.Radiobutton(
            frame_selection,
            text="Target 2",
            variable=visualize_target,
            value=2,
            command=lambda: updateTargetImage(images[1], imagePanel),
        )
    )
    radio.append(
        tk.Radiobutton(
            frame_selection,
            text="Target 3",
            variable=visualize_target,
            value=3,
            command=lambda: updateTargetImage(images[2], imagePanel),
        )
    )
    radio[0].grid(row=0, column=0, padx=10, pady=5)
    radio[1].grid(row=1, column=0, padx=10, pady=5)
    radio[2].grid(row=2, column=0, padx=10, pady=5)

    # --- Buttons for correlation scripts ---
    lfCorrelations = tk.LabelFrame(main_window, text="Correlations")
    lfCorrelations.grid(row=0, column=0, padx=10, pady=5)
    correlationTarget1Button = tk.Button(
        lfCorrelations,
        text="Correlation target 1",
        command=correlationTarget1Callback,
    )
    correlationTarget2Button = tk.Button(
        lfCorrelations,
        text="Correlation target 2",
        command=correlationTarget2Callback,
    )
    correlationTarget3Button = tk.Button(
        lfCorrelations,
        text="Correlation target 3",
        command=correlationTarget3Callback,
    )
    correlationTarget1Button.grid(row=0, column=0, padx=10, pady=5)
    correlationTarget2Button.grid(row=1, column=0, padx=10, pady=5)
    correlationTarget3Button.grid(row=2, column=0, padx=10, pady=5)

    # --- Some headers and exit button text ---
    mainApplicationLabel = tk.Label(
        main_window, text="HMCFWI visualization\r\nGebraad et al., 2019"
    )
    mainApplicationLabel.grid(row=0, column=2, padx=10)
    exitButton = tk.Button(main_window, text="Exit", command=exitCallback)
    exitButton.grid(row=0, column=5, padx=0, pady=5)

    main_window.mainloop()

    exit(0)
