import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from ttkwidgets import CheckboxTreeview

from VideoProcessor import VideoProcessor
from movement.SetOfMovements import SetOfMovements
from movement.Movement import Movement
from movement.MovementError import MovementError

from utils.Utils import Utils

import os
import threading
import PIL.Image
import PIL.ImageTk

from movement.XmlGenerator import XmlGenerator

script_dir = os.path.dirname(__file__)

class GetTemplatesFromVideo:

    def create_main_frame(self):
        main_frame = tk.Frame(self.root)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.pack()
        return main_frame

    @staticmethod
    def create_video_frame(main_frame):
        video_frame = tk.Frame(main_frame)

        video_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW + tk.NS)

        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=2)
        main_frame.rowconfigure(1, weight=2)
        main_frame.rowconfigure(2, weight=2)

        return video_frame

    @staticmethod
    def create_video_canvas(video_frame):
        video_canvas = tk.Canvas(video_frame,
                                 bd=0,
                                 highlightthickness=0,
                                 width=512,
                                 height=384,
                                 background="white")
        video_canvas.pack()
        return video_canvas

    def create_list_of_movements_frame(self, main_frame):
        list_of_movements_frame = tk.Frame(main_frame)

        list_box_label = tk.Label(list_of_movements_frame, text="List of Movements:")
        list_box_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        button_remove_movement = ttk.Button(
            list_of_movements_frame,
            text="Remove",
            command=self.remove_movement
        )
        button_remove_movement.grid(row=2, column=0, padx=5, pady=5, rowspan=2, sticky=tk.N + tk.E)

        list_of_movements_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW + tk.NS)
        list_of_movements_frame.columnconfigure(0, weight=2)
        list_of_movements_frame.columnconfigure(1, weight=0)
        list_of_movements_frame.rowconfigure(0, weight=0)
        list_of_movements_frame.rowconfigure(1, weight=2)

        return list_of_movements_frame

    @staticmethod
    def create_listbox_movements(list_of_movements_frame):
        listbox_movements = tk.Listbox(list_of_movements_frame, width=40)
        listbox_movements.grid(row=1, column=0, sticky=tk.NS)

        scrollbar = tk.Scrollbar(list_of_movements_frame)
        scrollbar.grid(row=1, column=1, sticky=tk.NS + tk.W)
        listbox_movements.config(yscrollcommand=scrollbar.set)
        return listbox_movements

    @staticmethod
    def create_list_of_key_points_frame(main_frame):
        list_of_key_points_frame = tk.Frame(main_frame)

        style = ttk.Style(list_of_key_points_frame)

        # remove the indicator in the treeview
        style.layout('Checkbox.Treeview.Item',
                     [('Treeitem.padding',
                       {'sticky': 'nswe',
                        'children': [('Treeitem.image', {'side': 'left', 'sticky': ''}),
                                     ('Treeitem.focus', {'side': 'left', 'sticky': '',
                                                         'children': [('Treeitem.text',
                                                                       {'side': 'left', 'sticky': ''})]})]})])
        # make it look more like a listbox
        style.configure('Checkbox.Treeview', borderwidth=1, relief='sunken')

        list_of_key_points_frame.columnconfigure(0, weight=2)
        list_of_key_points_frame.columnconfigure(1, weight=0)
        list_of_key_points_frame.rowconfigure(0, weight=0)
        list_of_key_points_frame.rowconfigure(1, weight=2)
        list_of_key_points_frame.grid(row=1, column=1, padx=5, pady=5, rowspan=6, sticky=tk.EW + tk.NS)

        return list_of_key_points_frame

    @staticmethod
    def create_checkbox_list_key_points(list_of_key_points_frame):
        checkbox_list_key_points = CheckboxTreeview(list_of_key_points_frame, show='tree')  # hide tree headings
        checkbox_list_key_points.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NS + tk.W)

        for key_point in Utils.get_landmarks_list():
            checkbox_list_key_points.insert('', 'end', iid=key_point, text=key_point)

        scrollbar = tk.Scrollbar(list_of_key_points_frame)
        scrollbar.grid(row=1, column=1, sticky=tk.NS + tk.W)

        checkbox_list_key_points.config(yscrollcommand=scrollbar.set)
        return checkbox_list_key_points

    @staticmethod
    def create_video_controller_frame(main_frame):
        video_controller_frame = tk.Frame(main_frame)

        video_controller_frame.rowconfigure(0, weight=1)
        video_controller_frame.columnconfigure(0, weight=0)
        video_controller_frame.columnconfigure(1, weight=0)
        video_controller_frame.columnconfigure(2, weight=0)
        video_controller_frame.columnconfigure(3, weight=2)
        video_controller_frame.columnconfigure(4, weight=0)
        video_controller_frame.columnconfigure(5, weight=0)
        video_controller_frame.columnconfigure(6, weight=0)
        video_controller_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return video_controller_frame

    def create_media_buttons(self, play_image, pause_image, beginning_image, ending_image, snapshot_image_start,
                             snapshot_image_end, video_controller_frame):
        play_button = tk.Button(video_controller_frame, text='Play', image=play_image, height=20, width=20,
                                command=self.play_video)
        play_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E + tk.S)
        play_button.config(state=tk.DISABLED)

        pause_button = tk.Button(video_controller_frame, text='Pause', image=pause_image, height=20,
                                 width=20,
                                 command=self.pause_video)
        pause_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E + tk.S)
        pause_button.config(state=tk.DISABLED)

        beginning_button = tk.Button(video_controller_frame, text='Beginning', image=beginning_image,
                                     height=20,
                                     width=20, command=self.to_beginning)
        beginning_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E + tk.S)
        beginning_button.config(state=tk.DISABLED)

        ending_button = tk.Button(video_controller_frame, text='Ending', image=ending_image, height=20,
                                  width=20,
                                  command=self.to_end)
        ending_button.grid(row=0, column=5, padx=5, pady=5, sticky=tk.E + tk.S)
        ending_button.config(state=tk.DISABLED)

        snapshot_button_start = tk.Button(video_controller_frame, text='Snapshot',
                                          image=snapshot_image_start, height=20,
                                          width=20, command=self.snapshot_start)
        snapshot_button_start.grid(row=0, column=6, padx=5, pady=5, sticky=tk.E + tk.S)
        snapshot_button_start.config(state=tk.DISABLED)

        snapshot_button_end = tk.Button(video_controller_frame, text='Snapshot', image=snapshot_image_end,
                                        height=20,
                                        width=20, command=self.snapshot_end)
        snapshot_button_end.grid(row=0, column=7, padx=5, pady=5, sticky=tk.E + tk.S)
        snapshot_button_end.config(state=tk.DISABLED)

        return play_button, pause_button, beginning_button, ending_button, snapshot_button_start, snapshot_button_end

    def create_slider_video_and_label_max_frames(self, controls_and_options_frame):
        slider_video = tk.Scale(controls_and_options_frame, from_=0, to=0, orient=tk.HORIZONTAL)
        slider_video.bind("<ButtonRelease-1>", self.update_video_from_slider)
        slider_video.grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW + tk.N)
        slider_video.config(state=tk.DISABLED)

        label_max_frames = tk.Label(controls_and_options_frame, text="Max: " + str(0))
        label_max_frames.grid(row=0, column=4, padx=5, pady=5, sticky=tk.E + tk.S)

        return slider_video, label_max_frames

    @staticmethod
    def create_set_info_frame(main_frame):
        set_info_frame = tk.Frame(main_frame)

        label_set_name = tk.Label(set_info_frame, text="Set Name: ")
        label_set_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        set_info_frame.rowconfigure(0, weight=1)
        set_info_frame.columnconfigure(0, weight=0)
        set_info_frame.columnconfigure(1, weight=2)
        set_info_frame.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return set_info_frame

    @staticmethod
    def create_entry_set_name(set_info_frame):
        entry_set_name = ttk.Entry(set_info_frame)
        entry_set_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.EW)

        return entry_set_name

    @staticmethod
    def create_set_description_frame(main_frame):
        set_description_frame = tk.Frame(main_frame)

        set_description_label = tk.Label(set_description_frame, text="Set Description: ")
        set_description_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        set_description_frame.rowconfigure(0, weight=1)
        set_description_frame.rowconfigure(1, weight=1)
        set_description_frame.columnconfigure(0, weight=1)
        set_description_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return set_description_frame

    @staticmethod
    def create_entry_set_description(set_description_frame):
        entry_set_description = ttk.Entry(set_description_frame)
        entry_set_description.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.EW)

        return entry_set_description

    @staticmethod
    def create_movement_name_frame(main_frame):
        movement_name_frame = tk.Frame(main_frame)

        label_name = tk.Label(movement_name_frame, text="Movement Name: ")
        label_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        movement_name_frame.rowconfigure(0, weight=1)
        movement_name_frame.columnconfigure(0, weight=0)
        movement_name_frame.columnconfigure(1, weight=2)
        movement_name_frame.grid(row=4, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return movement_name_frame

    @staticmethod
    def create_entry_movement_name(movement_name_frame):
        entry_movement_name = ttk.Entry(movement_name_frame)
        entry_movement_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.EW)

        return entry_movement_name

    @staticmethod
    def create_start_and_end_frames_frame(main_frame):
        start_and_end_frames_frame = tk.Frame(main_frame)

        start_frame_label = tk.Label(start_and_end_frames_frame, text="Start Frame: ")
        start_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky=tk.N + tk.W)

        end_frame_name = tk.Label(start_and_end_frames_frame, text="End Frame: ")
        end_frame_name.grid(row=0, column=2, padx=0, pady=0, sticky=tk.N + tk.E)

        start_and_end_frames_frame.rowconfigure(0, weight=1)
        start_and_end_frames_frame.columnconfigure(0, weight=1)
        start_and_end_frames_frame.columnconfigure(1, weight=1)
        start_and_end_frames_frame.columnconfigure(2, weight=1)
        start_and_end_frames_frame.columnconfigure(3, weight=1)
        start_and_end_frames_frame.grid(row=5, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return start_and_end_frames_frame

    @staticmethod
    def create_entries_start_and_end_frames(start_and_end_frames_frame):
        entry_start_frame = ttk.Entry(start_and_end_frames_frame)
        entry_start_frame.grid(row=0, column=1, padx=0, pady=0, sticky=tk.N + tk.W)

        entry_end_frame = ttk.Entry(start_and_end_frames_frame)
        entry_end_frame.grid(row=0, column=3, padx=0, pady=0, sticky=tk.N + tk.E)

        return entry_start_frame, entry_end_frame

    @staticmethod
    def create_movement_description_frame(main_frame):
        movement_description_frame = tk.Frame(main_frame)

        description_label = tk.Label(movement_description_frame, text="Movement Description: ")
        description_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        movement_description_frame.rowconfigure(0, weight=1)
        movement_description_frame.rowconfigure(1, weight=1)
        movement_description_frame.columnconfigure(0, weight=1)
        movement_description_frame.grid(row=6, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return movement_description_frame

    @staticmethod
    def create_entry_movement_description(movement_description_frame):
        entry_movement_description = ttk.Entry(movement_description_frame)
        entry_movement_description.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.EW)

        return entry_movement_description

    @staticmethod
    def create_movement_feedback_message_frame(main_frame):
        movement_feedback_message_frame = tk.Frame(main_frame)

        feedback_label = tk.Label(movement_feedback_message_frame, text="Movement Feedback Message: ")
        feedback_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        movement_feedback_message_frame.rowconfigure(0, weight=1)
        movement_feedback_message_frame.rowconfigure(1, weight=1)
        movement_feedback_message_frame.columnconfigure(0, weight=1)
        movement_feedback_message_frame.grid(row=7, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return movement_feedback_message_frame

    @staticmethod
    def create_entry_movement_feedback_message(movement_feedback_frame):
        entry_movement_feedback_message = ttk.Entry(movement_feedback_frame)
        entry_movement_feedback_message.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.EW)

        return entry_movement_feedback_message

    def create_is_error_and_parent_frame(self, main_frame):
        is_error_and_parent_frame = tk.Frame(main_frame)

        checkbox_is_error = ttk.Checkbutton(is_error_and_parent_frame, text="Is Error?",
                                            variable=self.error_checkbox_value,
                                            command=self.is_error_clicked)
        checkbox_is_error.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.W)

        parent_label = tk.Label(is_error_and_parent_frame, text="Parent: ")
        parent_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E)

        is_error_and_parent_frame.rowconfigure(0, weight=1)
        is_error_and_parent_frame.columnconfigure(0, weight=1)
        is_error_and_parent_frame.columnconfigure(1, weight=1)
        is_error_and_parent_frame.columnconfigure(2, weight=1)
        is_error_and_parent_frame.grid(row=8, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return is_error_and_parent_frame

    @staticmethod
    def create_combobox_parent(is_error_and_parent_frame):
        combobox_parent = ttk.Combobox(is_error_and_parent_frame, state="readonly", values=[""])
        combobox_parent.config(state="disabled")
        combobox_parent.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.E)

        return combobox_parent

    @staticmethod
    def create_button_add_movement_frame(main_frame):
        add_movement_frame = tk.Frame(main_frame)

        add_movement_frame.rowconfigure(0, weight=1)
        add_movement_frame.columnconfigure(0, weight=1)
        add_movement_frame.grid(row=9, column=0, padx=5, pady=5, sticky=tk.EW + tk.N)

        return add_movement_frame

    def create_button_add_movement(self, add_movement_frame):
        button_add_movement = ttk.Button(
            add_movement_frame,
            text="Add Movement",
            command=self.add_movement
        )
        button_add_movement.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E)

        return button_add_movement

    @staticmethod
    def create_footer_frame(main_frame):
        footer_frame = tk.Frame(main_frame)

        footer_frame.rowconfigure(0, weight=1)
        footer_frame.columnconfigure(0, weight=1)
        footer_frame.grid(row=10, column=0, padx=5, pady=5, columnspan=2, sticky=tk.EW + tk.N)

        return footer_frame

    @staticmethod
    def create_progress_bar_and_progress_label(footer_frame):
        progress_bar_label = tk.Label(footer_frame, text="")
        progress_bar_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E)

        progress_bar = ttk.Progressbar(footer_frame, orient='horizontal', mode='indeterminate', length=140)
        progress_bar.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E)

        return progress_bar, progress_bar_label

    def __init__(self):
        self.set_of_movements = SetOfMovements()

        # After tkinter job.
        self._job = None

        # Create window.
        self.root = tk.Tk()
        self.root.title("Template Creator")

        # Window min dimensions.
        window_width = 800
        window_height = 910

        # Default values.
        self.error_checkbox_value = tk.IntVar(value=0)
        self.processing_video = False

        # Set dimensions.
        self.set_dimensions(window_width, window_height)

        # Set menu bar.
        self.set_menu_bar()

        # Video processor.
        self.video_processor = VideoProcessor()

        # Video canvas.
        self.video_canvas = None

        # GUI Setup.
        main_frame = self.create_main_frame()

        video_frame = self.create_video_frame(main_frame)
        self.video_canvas = self.create_video_canvas(video_frame)

        list_of_movements_frame = self.create_list_of_movements_frame(main_frame)
        self.listbox_movements = self.create_listbox_movements(list_of_movements_frame)
        self.listbox_movements.bind('<Double-1>', self.update_view)
        list_of_key_points_frame = self.create_list_of_key_points_frame(main_frame)
        self.checkbox_list_key_points = self.create_checkbox_list_key_points(list_of_key_points_frame)

        video_controller_frame = self.create_video_controller_frame(main_frame)

        self.play_image = PIL.Image.open('assets/play.png')
        self.play_image = self.play_image.resize((20, 20))
        self.play_image = PIL.ImageTk.PhotoImage(self.play_image)
        self.pause_image = PIL.Image.open('assets/pause.png')
        self.pause_image = self.pause_image.resize((20, 20))
        self.pause_image = PIL.ImageTk.PhotoImage(self.pause_image)
        self.beginning_image = PIL.Image.open('assets/beginning.png')
        self.beginning_image = self.beginning_image.resize((20, 20))
        self.beginning_image = PIL.ImageTk.PhotoImage(self.beginning_image)
        self.ending_image = PIL.Image.open('assets/ending.png')
        self.ending_image = self.ending_image.resize((20, 20))
        self.ending_image = PIL.ImageTk.PhotoImage(self.ending_image)
        self.snapshot_image_start = PIL.Image.open('assets/snapshot_start.png')
        self.snapshot_image_start = self.snapshot_image_start.resize((20, 20))
        self.snapshot_image_start = PIL.ImageTk.PhotoImage(self.snapshot_image_start)
        self.snapshot_image_end = PIL.Image.open('assets/snapshot_end.png')
        self.snapshot_image_end = self.snapshot_image_end.resize((20, 20))
        self.snapshot_image_end = PIL.ImageTk.PhotoImage(self.snapshot_image_end)
        (self.play_button,
         self.pause_button,
         self.beginning_button,
         self.ending_button,
         self.snapshot_button_start,
         self.snapshot_button_end) = self.create_media_buttons(self.play_image,
                                                               self.pause_image,
                                                               self.beginning_image,
                                                               self.ending_image,
                                                               self.snapshot_image_start,
                                                               self.snapshot_image_end,
                                                               video_controller_frame)
        (self.slider_video,
         self.label_max_frames) = self.create_slider_video_and_label_max_frames(video_controller_frame)

        set_info_frame = self.create_set_info_frame(main_frame)
        self.entry_set_name = self.create_entry_set_name(set_info_frame)

        set_description_frame = self.create_set_description_frame(main_frame)
        self.entry_set_description = self.create_entry_set_description(set_description_frame)

        movement_name_frame = self.create_movement_name_frame(main_frame)
        self.entry_movement_name = self.create_entry_movement_name(movement_name_frame)

        start_and_end_frames_frame = self.create_start_and_end_frames_frame(main_frame)
        (self.entry_start_frame, self.entry_end_frame) = self.create_entries_start_and_end_frames(
            start_and_end_frames_frame)

        movement_description_frame = self.create_movement_description_frame(main_frame)
        self.entry_movement_description = self.create_entry_movement_description(movement_description_frame)

        movement_feedback_message_frame = self.create_movement_feedback_message_frame(main_frame)
        self.entry_movement_feedback_message = self.create_entry_movement_feedback_message(
            movement_feedback_message_frame)

        is_error_and_parent_frame = self.create_is_error_and_parent_frame(main_frame)
        self.combobox_parent = self.create_combobox_parent(is_error_and_parent_frame)

        button_add_movement_frame = self.create_button_add_movement_frame(main_frame)
        self.button_add_movement = self.create_button_add_movement(button_add_movement_frame)

        footer_frame = self.create_footer_frame(main_frame)
        (self.progress_bar, self.progress_bar_label) = self.create_progress_bar_and_progress_label(footer_frame)

        # Footer.
        # Initialize video.
        self.update_video()

        # Start GUI.
        self.root.mainloop()

    def is_error_clicked(self):
        if bool(self.error_checkbox_value.get()):
            self.combobox_parent.config(state="readonly")
        else:
            self.combobox_parent.config(state="disabled")

    def set_dimensions(self, window_width, window_height):
        # Screen dimensions.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get center point.
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2) - 30

        # Set window in center of screen.
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Size properties.
        self.root.resizable(True, True)
        self.root.minsize(window_width, window_height)

    def set_menu_bar(self):
        # Create menu bar.
        menu_bar = tk.Menu()

        # Add file.
        menu_file = tk.Menu(menu_bar, tearoff=False)

        menu_file.add_command(
            label="Load Video...",
            command=self.load_video
        )
        menu_file.add_command(
            label="Save Template...",
            command=self.save_template
        )
        menu_bar.add_cascade(menu=menu_file, label="File")

        # Add Exit.
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.root.destroy)

        # Add menu bar.
        self.root.config(menu=menu_bar)

    def load_video(self):
        # Home directory as default for selector.
        home = os.path.expanduser('~')

        # Supported formats.
        filetypes = (
            ('mp4', '*.mp4'),
            ('avi', '*.avi'),
            ('mov', '*.mov'),
            ('mpeg', '*.mpeg'),
            ('flv', '*.flv'),
            ('wmv', '*.wmv')
        )

        # Get file path from user.
        video_path = fd.askopenfilename(
            title='Select a video file',
            filetypes=filetypes,
            initialdir=home,
        )

        threading.Thread(target=self.process_video, args=[video_path]).start()

        # Print file name in terminal.
        print("File Name:", video_path)

    def process_video(self, video_path):
        self.video_processor = VideoProcessor(video_path)

        # Update max frames slider.
        self.pause_video()

        # Go to beginning.
        self.to_beginning()

        self.start_progress_bar("Processing Video...")
        self.processing_video = True

        # Process full video using mediapipewrapper.
        json_template = self.video_processor.process_full_video_mediapipe()
        self.processing_video = False
        self.stop_progress_bar("Video Processed.")

        self.video_processor = VideoProcessor("processed.avi")

        self.slider_video.configure(to=self.video_processor.num_frames)
        self.label_max_frames.configure(text="Max: " + str(self.video_processor.num_frames))

        self.pause_video()

        # Go to beginning.
        self.to_beginning()

        # Print file name in terminal.
        print("File Name:", "processed.avi")

        # Save template into set of movements.
        self.set_of_movements.set_template(json_template)

    def check_errors_set(self):
        check_ok = True

        # Check if there is name.
        if self.entry_set_name.get() == "":
            check_ok = False
            messagebox.showerror('Python Error', 'Error: Set name is empty!')
        elif self.entry_set_description.get() == "":
            check_ok = False
            messagebox.showerror('Python Error', 'Error: Set description is empty!')

        return check_ok

    def save_template(self):
        check_ok = self.check_errors_set()

        if check_ok:
            self.set_of_movements.set_name(self.entry_set_name.get())
            self.set_of_movements.set_description(self.entry_set_description.get())
            generator = XmlGenerator(self.set_of_movements)
            generator.generate()

    def update_video(self):
        # Update slider value.
        self.slider_video.set(self.video_processor.get_current_frame_number())

        # If there is a frame, update view.
        self.show_frame()

        self._job = self.root.after(30, self.update_video)

    def pause_video(self):
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None

    def play_video(self):
        self.update_video()

    def to_beginning(self):
        # Set to first frame.
        self.video_processor.set_to_frame(0)

        # Set slider to first frame.
        self.slider_video.set(0)

        # Show first frame.
        self.show_frame()

    def to_end(self):
        # Set to last frame. Minus one because when you show the frame, you increment it.
        self.video_processor.set_to_frame(self.video_processor.num_frames - 1)

        # Set slider to first frame.
        self.slider_video.set(self.video_processor.num_frames)

        # Show last frame.
        self.show_frame()

    def update_video_from_slider(self, event):
        # Set to last frame. Minus one because when you show the frame, you increment it.
        if self.slider_video.get() is self.video_processor.num_frames:
            self.video_processor.set_to_frame(self.slider_video.get() - 1)
        else:
            self.video_processor.set_to_frame(self.slider_video.get())

        # Set slider to first frame.
        self.slider_video.set(self.slider_video.get())

        # Show last frame.
        self.show_frame()

    def show_frame(self):
        # Get frame.
        ret, frame = self.video_processor.get_frame()
        # If there is a frame, update view.
        if ret:
            # Create PIL image from frame.
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame).resize((512, 384), PIL.Image.ANTIALIAS))

            # To prevent garbage collector from removing it.
            self.root.one = photo

            # Show image in canvas.
            self.video_canvas.create_image((0, 0), image=photo, anchor=tk.NW)

    def check_errors_movement(self):
        check_ok = True
        update = False

        # List of existing movements.
        listbox_movements = self.listbox_movements.get(0, "end")
        current_movement = self.set_of_movements.get_movement(self.entry_movement_name.get())

        # Check problems when is_error is checked.
        if self.error_checkbox_value.get():
            # Check if there are available parent movements.
            if len(self.set_of_movements.get_movement_names()) == 0:
                check_ok = False
                messagebox.showerror('Python Error', 'Error: There are no possible parents, unselect is_error!')
            # Check if parent selected.
            elif self.combobox_parent.get() == "":
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Movement is an error, but a parent has not been selected!')
            # Check if parent is valid.
            elif self.combobox_parent.get() not in self.set_of_movements.get_movement_names():
                check_ok = False
                messagebox.showerror('Python Error', 'Error: The parent movement is not a parent!')
            # Check parent is not the own movement.
            elif self.combobox_parent.get() == self.entry_movement_name.get():
                check_ok = False
                messagebox.showerror('Python Error', 'Error: A movement cannot be its own parent!')
            # Check if has children.
            elif current_movement is not None and len(current_movement.get_movement_errors()) != 0:
                check_ok = False
                messagebox.showerror('Python Error', 'Error: This movement has children, cannot set a parent!')

        if check_ok:
            # Check if there is name.
            if self.entry_movement_name.get() == "":
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Movement name is empty!')
            # Check if there is start frame. and if it is a digit.
            elif self.entry_start_frame.get() == "":
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Start frame is empty!')
            # Check if start_frame is a digit.
            elif not self.entry_start_frame.get().isdigit():
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Start frame is not a valid number!')
            # Check if there is end frame and if it is a digit.
            elif self.entry_end_frame.get() == "":
                check_ok = False
                messagebox.showerror('Python Error', 'Error: End frame is empty!')
            # Check if end_frame is a digit.
            elif not self.entry_end_frame.get().isdigit():
                check_ok = False
                messagebox.showerror('Python Error', 'Error: End frame is not a valid number!')
            # Check if start frame is smaller than end frame.
            elif int(self.entry_start_frame.get()) > int(self.entry_end_frame.get()):
                check_ok = False
                messagebox.showerror('Python Error', 'Error: End frame should be greater than start frame!')
            # Check if there is movement description.
            elif self.entry_movement_description.get() == "":
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Movement description is empty!')
            # Check if there is feedback message.
            elif self.entry_movement_feedback_message.get() == "":
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Movement feedback message is empty!')
            # Check at least one key point is selected.
            elif len(self.checkbox_list_key_points.get_checked()) == 0:
                check_ok = False
                messagebox.showerror('Python Error', 'Error: Select at least one key point!')
            # Check if movement name already exists.
            elif listbox_movements != () and self.entry_movement_name.get() in listbox_movements:
                update = False
                check_ok = False
                answer = tk.messagebox.askokcancel(
                    title='Confirmation',
                    message='A movement with this name already exists. Update it?',
                    icon=tk.messagebox.QUESTION)
                if answer:
                    update = True
                    check_ok = True

        return update, check_ok

    def add_movement(self):
        is_error = self.error_checkbox_value.get()

        if not is_error:
            # Is a regular movement.
            movement = Movement()
        else:
            # Is an error movement.
            movement = MovementError()

        update, check_ok = self.check_errors_movement()

        if update and check_ok:
            # Retrieve existing movement (can be error or not, maybe the user wants to change it).
            old_movement = None
            old_movement_parent = None
            movement_list = self.set_of_movements.get_movements()
            for mov in movement_list:
                if old_movement is not None:
                    break
                if mov.get_name() == self.entry_movement_name.get():
                    old_movement = mov
                    old_movement_parent = None
                for mov_error in mov.get_movement_errors():
                    if old_movement is not None:
                        break
                    if mov_error.get_name() == self.entry_movement_name.get():
                        old_movement = mov_error
                        old_movement_parent = mov

            if old_movement_parent is None:

                # If it was not an error, and now it is an error, remove and create a movement_error.
                if is_error:
                    # Remove from set.
                    self.set_of_movements.remove_movement(old_movement.get_name())

                    # Create movement error with same name.
                    old_movement = MovementError()
                    old_movement.set_name(self.entry_movement_name.get())

                    # Add to parent movement.
                    parent_name = self.combobox_parent.get()
                    parent = self.set_of_movements.get_movement(parent_name)
                    parent.add_movement_error(old_movement)

                    # Remove from list of parents.
                    self.combobox_parent['values'] = self.set_of_movements.get_movement_names()

            else:

                # If it was an error, and now it is not, remove from parent and insert as movement.
                if not is_error:
                    old_movement_parent.remove_movement_error(old_movement.get_name())

                    # Create movement error with same name.
                    old_movement = Movement()
                    old_movement.set_name(self.entry_movement_name.get())

                    # Add to set.
                    self.set_of_movements.add_movement(old_movement)

                    # Add to list of parents.
                    self.combobox_parent['values'] = self.set_of_movements.get_movement_names()

                # If it was an error, and it is still an error, check if the parent is the same and update.
                else:
                    parent_name = self.combobox_parent.get()

                    # If parent has changed, update, remove from old parent, and add to new parent.
                    if parent_name != old_movement_parent.get_name():
                        old_movement_parent.remove_movement_error(old_movement.get_name())
                        new_parent = self.set_of_movements.get_movement(parent_name)
                        new_parent.add_movement_error(old_movement)

            # If it was not an error and still not an error, just update info.
            old_movement.set_description(self.entry_movement_description.get())
            old_movement.set_feedback_message(self.entry_movement_feedback_message.get())
            old_movement.set_start_frame(self.entry_start_frame.get())
            old_movement.set_end_frame(self.entry_end_frame.get())

            # Add key points.
            old_movement.key_points.clear()
            for key_point in self.checkbox_list_key_points.get_checked():
                old_movement.add_keypoint(key_point)

        elif not update and check_ok:
            # Add information about the movement.
            movement.set_name(self.entry_movement_name.get())
            movement.set_description(self.entry_movement_description.get())
            movement.set_feedback_message(self.entry_movement_feedback_message.get())
            movement.set_start_frame(self.entry_start_frame.get())
            movement.set_end_frame(self.entry_end_frame.get())

            if not is_error:
                # Add to set of movements.
                self.set_of_movements.add_movement(movement)

                # Add to list of possible parents.
                self.combobox_parent['values'] = self.set_of_movements.get_movement_names()
            else:
                # Add to parent movement.
                parent_name = self.combobox_parent.get()
                parent = self.set_of_movements.get_movement(parent_name)
                parent.add_movement_error(movement)

            # Add key points.
            movement.key_points.clear()
            for keypoint in self.checkbox_list_key_points.get_checked():
                movement.add_keypoint(keypoint)

            # Add to list of movements.
            self.listbox_movements.insert(0, movement.get_name())

    def remove_movement(self):
        # Get index and name.
        index = self.listbox_movements.curselection()
        name = self.listbox_movements.get(index)

        # Remove from listbox.
        movement = self.set_of_movements.get_movement(name)
        self.listbox_movements.delete(index)
        if isinstance(movement, Movement):
            movement_error_names = movement.get_movement_error_names()
            for movement_error in movement_error_names:
                self.listbox_movements.delete(self.listbox_movements.get(0, "end").index(movement_error))

        # Remove from set of movements and from parent.
        if not self.set_of_movements.remove_movement(name):
            self.set_of_movements.remove_movement_error(name)

        self.combobox_parent['values'] = self.set_of_movements.get_movement_names()

    def start_progress_bar(self, message):
        self.progress_bar_label.config(text=message)
        self.progress_bar.start()
        self.change_buttons_state(tk.DISABLED)

    def stop_progress_bar(self, message):
        self.progress_bar_label.config(text=message)
        self.progress_bar.stop()
        self.change_buttons_state(tk.NORMAL)

    def change_buttons_state(self, state):
        self.play_button.config(state=state)
        self.pause_button.config(state=state)
        self.beginning_button.config(state=state)
        self.slider_video.config(state=state)
        self.ending_button.config(state=state)
        self.snapshot_button_start.config(state=state)
        self.snapshot_button_end.config(state=state)

    def snapshot_start(self):
        print(self.video_processor.get_current_frame_number())
        self.entry_start_frame.delete(0, tk.END)
        self.entry_start_frame.insert(0, self.video_processor.get_current_frame_number())

    def snapshot_end(self):
        print(self.video_processor.get_current_frame_number())
        self.entry_end_frame.delete(0, tk.END)
        self.entry_end_frame.insert(0, self.video_processor.get_current_frame_number())

    def update_view(self, event):
        # Get index and name.
        index = self.listbox_movements.curselection()
        name = self.listbox_movements.get(index)

        # Retrieve existing movement (can be error or not, maybe the user wants to change it).
        movement = None
        movement_parent = None
        movement_list = self.set_of_movements.get_movements()
        for mov in movement_list:
            if movement is not None:
                break
            if mov.get_name() == name:
                movement = mov
                movement_parent = None
            for mov_error in mov.get_movement_errors():
                if movement is not None:
                    break
                if mov_error.get_name() == name:
                    movement = mov_error
                    movement_parent = mov

        self.entry_movement_name.delete(0, tk.END)
        self.entry_movement_name.insert(0, movement.get_name())
        self.entry_movement_description.delete(0, tk.END)
        self.entry_movement_description.insert(0, movement.get_description())
        self.entry_movement_feedback_message.delete(0, tk.END)
        self.entry_movement_feedback_message.insert(0, movement.get_feedback_message())
        self.entry_start_frame.delete(0, tk.END)
        self.entry_start_frame.insert(0, movement.get_start_frame())
        self.entry_end_frame.delete(0, tk.END)
        self.entry_end_frame.insert(0, movement.get_end_frame())

        if movement_parent is not None:
            self.error_checkbox_value.set(1)
            self.combobox_parent.set(movement_parent.get_name())
            self.combobox_parent.config(state="readonly")
        else:
            self.error_checkbox_value.set(0)
            self.combobox_parent.config(state="disabled")

        # TODO CHANGE CHECKBOX OF KEYFRAMES
