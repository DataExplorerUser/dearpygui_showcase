import dearpygui.core as dpg
import dearpygui.simple as dpgs
from multiprocessing import Process
from pathlib import Path
import types

def start_program(file_path): # start one of the demo programs
    p = Path(file_path)
    ns = types.ModuleType(p.name)
    exec(compile(p.read_text(encoding='utf-8'), str(p), 'exec'), ns.__dict__)

def program_process(arg1, arg2): # decide which demo program to run
    path_name = 'demo_' + arg1 + arg2 + '/main.py'
    start_program(path_name)

def start_process(sender, data):
    test_process = Process(target=program_process, args=data)
    test_process.start()

def auto_center(sender, data):

    # adjust the height of the body window on resize
    # so that the scrolling works correctly
    
    header_window_height = 100
    window_height = dpg.get_main_window_size()[1]
    body_window_height = window_height - header_window_height - 40 # 100 ~ dpgs.get_item_height('header window')
    dpgs.set_item_height('body window', body_window_height) 

    # make the width header and body windows equal to the width of the main window
    window_width = dpg.get_main_window_size()[0] # dpgs.get_item_width('main window')
    dpgs.set_item_width('header window', window_width)
    dpgs.set_item_width('body window', window_width)

    # align header
    item_name = dpg.get_item_children("item-to-center")
    item_width = dpgs.get_item_width('dearpygui logo') # 200
    left = int(window_width/2 - item_width/2 - 23)
    minimum_left_padding = 50
    if left < minimum_left_padding:
        left = minimum_left_padding
    dpgs.set_item_width('left-spacer', left)

    # space between columns
    minimum_space_between_columns = 100
    space_between_columns = int(window_width * 0.1)
    if space_between_columns < minimum_space_between_columns:
        space_between_columns = minimum_space_between_columns
    dpgs.set_item_width('space between columns', space_between_columns)
    dpgs.set_item_width('space between columns 2', space_between_columns)
    dpgs.set_item_width('space between columns 3', space_between_columns)

    # align body containing tiles
    item_width = dpgs.get_item_width('Demo 1')
    left = int( (   (window_width - 1200 - ((space_between_columns - minimum_space_between_columns)/2) ) / 2))      # TO CORRECT FOR SPACE BETWEEN COLUMNS
    minimum_left_padding = 50
    if left < minimum_left_padding:
        left = minimum_left_padding
    dpgs.set_item_width("left-spacer-tiles", left)

if __name__ == '__main__':

    # style settings
    dpg.set_main_window_size(1920, 1080)
    dpg.set_main_window_title("DearPy Gui Showcase")
    button_width=500
    button_height=300
    header_height=100
    dpg.add_additional_font('resources/glacial_font.otf', 22)
    dpg.set_theme_item(0, 0, 0, 0, 255) # set font colour 
    dpg.set_theme_item(2, 255, 255, 255, 255) # set background colour (mvGuiCol_WindowBg)

    # main window
    with dpgs.window('main window', x_pos=0, y_pos=0, width=1600, height=1200,
            autosize=False, no_resize=True, no_title_bar=True, no_move=True, no_scrollbar=False,
            no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True, no_bring_to_front_on_focus=False,
            no_close=True, no_background=False, show=True):

        # this is to remove style borders, padding and spacings from the main window 
        # which mess up spacing calculation
        dpg.set_item_style_var("main window", dpg.mvGuiStyleVar_WindowBorderSize, [0])
        dpg.set_item_style_var("main window", dpg.mvGuiStyleVar_WindowPadding, [0,0])
        dpg.set_item_style_var("main window", dpg.mvGuiStyleVar_ItemSpacing, [0,0])
        dpg.set_item_style_var("main window", dpg.mvGuiStyleVar_ItemInnerSpacing, [0,0])
        dpg.set_style_child_border_size(0.00)

    # place dearpygui logo on top. no scrollbars, therefore separate window
    with dpgs.window('header window', x_pos=0, y_pos=0, width=1600, height=header_height, autosize=True, no_resize=True,
        no_title_bar=True, no_move=True, no_scrollbar=True, no_collapse=True, horizontal_scrollbar=False,
        no_focus_on_appearing=True, no_bring_to_front_on_focus=False, no_close=True, no_background=True,
         show=True):

        with dpgs.child("center-group", autosize_x=True, autosize_y=True, no_scrollbar=True, menubar=False, border=False):
            dpg.add_dummy(name="left-spacer", width=0)
            dpg.add_same_line()
            with dpgs.group("item-to-center"):  
                dpg.add_image(name='dearpygui logo', value='resources/dearpygui_horizontal.png')

    # window with tiles and scrollbars
    with dpgs.window('body window', x_pos=0, y_pos=header_height, width=1600, height=1200,
            autosize=True, no_resize=True, no_title_bar=True, no_move=True, no_scrollbar=False,
            no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True, no_bring_to_front_on_focus=False,
            no_close=True, no_background=True, show=True):  # autosize=True --> Scrollbar is shown if True

        # remove style borders, padding and spacings from the body window
        # which mess up spacing calculation
        dpg.set_item_style_var("body window", dpg.mvGuiStyleVar_WindowBorderSize, [0])
        dpg.set_item_style_var("body window", dpg.mvGuiStyleVar_WindowPadding, [0,0])
       
        # scollbar settings
        dpg.set_theme_item(dpg.mvGuiCol_ScrollbarBg, 255, 255, 255, 135)           # white scrollbar background colour
        dpg.set_theme_item(dpg.mvGuiCol_ScrollbarGrab, 180, 180, 180, 255)         # light gray scrollbar when not in use
        dpg.set_theme_item(dpg.mvGuiCol_ScrollbarGrabHovered,  66, 160, 250, 150)  # light blue scrollbar when hovering over scrollbar
        dpg.set_theme_item(dpg.mvGuiCol_ScrollbarGrabActive, 66, 150, 250, 200)    # dark blue scrollbar when clicking on scrollbar
        dpg.set_style_scrollbar_size(17.00)
        dpg.set_style_scrollbar_rounding(12.00)

        # add child to enable scrollbars
        with dpgs.child('center-group-tiles', autosize_x=True, autosize_y=True, no_scrollbar=False, menubar=False,
            border=False, horizontal_scrollbar=False):
            
            dpg.add_dummy(name='left-spacer-tiles', width=0)
            dpg.add_same_line()
            with dpgs.group('item-to-center-tiles'):

                dpg.add_spacing(count=10)

                #
                # TILE BLOCK 1
                # group added for consistent horizontal placement
                #
                with dpgs.group(name='button group 1', horizontal=True, horizontal_spacing=0):

                    with dpgs.group(name='Tile 1', horizontal=False, horizontal_spacing=0):

                        dpg.add_image_button('Demo 1', value='resources/tile_01.png', height=button_height, width=button_width, 
                        frame_padding=5, background_color=[0,0,0,0], callback=start_process, callback_data='01')

                        with dpgs.group(name='tagline 1', horizontal=True, horizontal_spacing=0):
                            dpg.add_text('  ')
                            dpg.add_image(name='item 1', value='resources/blue_arrow.png')
                            dpg.add_text("\nText, sliders, buttons, menu's, images and more -- Sweet.")
                    
                    dpg.add_dummy(name='space between columns', width=0)

                    with dpgs.group(name='Tile 2', horizontal=False, horizontal_spacing=0):

                        dpg.add_image_button('Demo 2', value='resources/tile_02.png', height=button_height, width=button_width, 
                        frame_padding=5, background_color=[0,0,0,0], callback=start_process, callback_data='02')

                        with dpgs.group(name='tagline 2', horizontal=True, horizontal_spacing=0):
                            dpg.add_text('  ')
                            dpg.add_image(name='item 2', value='resources/blue_arrow.png')
                            dpg.add_text('\nReal-time and interactive graphs -- Sure.')

                # add vertical spacing between tile groups
                dpg.add_spacing(count=25)

                #
                # TILE BLOCK 2
                # 
                #
                with dpgs.group(name='button group 2', horizontal=True, horizontal_spacing=0):

                    with dpgs.group(name='Tile 3', horizontal=False, horizontal_spacing=0):

                        dpg.add_image_button('Demo 3', value='resources/tile_03.png', height=button_height, width=button_width, 
                        frame_padding=5, background_color=[0,0,0,0], callback=start_process, callback_data='03')

                        with dpgs.group(name='tagline 3', horizontal=True, horizontal_spacing=0):
                            dpg.add_text('  ')
                            dpg.add_image(name='item 3', value='resources/blue_arrow.png')
                            dpg.add_text("\nDocs, logger and style editor included? Yes, ma'am.")
                    
                    dpg.add_dummy(name='space between columns 2', width=0)

                    with dpgs.group(name='Tile 4', horizontal=False, horizontal_spacing=0):

                        dpg.add_image_button('Demo 4', value='resources/tile_04.png', height=button_height, width=button_width, 
                        frame_padding=5, background_color=[0,0,0,0], callback=start_process, callback_data='04')

                        with dpgs.group(name='tagline 4', horizontal=True, horizontal_spacing=0):
                            dpg.add_text('  ')
                            dpg.add_image(name='item 4', value='resources/blue_arrow.png')
                            dpg.add_text('\nTables with millions of rows? No problem!')
                    
                # add vertical spacing between tile groups
                dpg.add_spacing(count=25)

                #
                # TILE BLOCK 3
                #
                #
                with dpgs.group(name='button group 3', horizontal=True, horizontal_spacing=0):

                    with dpgs.group(name='Tile 5', horizontal=False, horizontal_spacing=0):

                        dpg.add_image_button('Demo 5', value='resources/tile_05.png', height=button_height, width=button_width, 
                        frame_padding=5, background_color=[0,0,0,0], callback=start_process, callback_data='05')

                        with dpgs.group(name='tagline 5', horizontal=True, horizontal_spacing=0):
                            dpg.add_text('  ')
                            dpg.add_image(name='item 5', value='resources/blue_arrow.png')
                            dpg.add_text("\nTagline 5")
                    
                    dpg.add_dummy(name='space between columns 3', width=0)

                    with dpgs.group(name='Tile 6', horizontal=False, horizontal_spacing=0):

                        dpg.add_image_button('Demo 6', value='resources/tile_06.png', height=button_height, width=button_width, 
                        frame_padding=5, background_color=[0,0,0,0], callback=start_process, callback_data='06')

                        with dpgs.group(name='tagline 6', horizontal=True, horizontal_spacing=0):
                            dpg.add_text('  ')
                            dpg.add_image(name='item 6', value='resources/blue_arrow.png')
                            dpg.add_text('\nTagline 6')

                # END OF TILES

                # add vertical spacing so last lines are shown when scrolling down
                dpg.add_spacing(count=8)
                
                # END OF BODY


    dpg.set_resize_callback(auto_center, handler='main window')
    # dpg.set_render_callback(auto_center)
    dpg.start_dearpygui(primary_window='main window')