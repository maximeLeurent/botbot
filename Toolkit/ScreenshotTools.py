import os
import win32gui, win32ui, win32con

def takeScreenshot(windowName, width, height, left, top, keepScreen=True, getText=False):
    """
        This function allow to take screenshot of a specific window designate
        by is name, you must also specify, the starting point (left, top) and
        the size (width, height) of the zone you want to extractself.
        Then you can decide to keep or not the generated file and choose to try
        to evaluate a text from this file with pytesseract prebuild method.

        :param windowName: The name of the window
        :type windowName: string
        :param width: The width of the zone you want to capture
        :type width: int
        :param height: The height of the zone you want to capture
        :type height: int
        :param left: The left position of starting point on top left corner
        :type left: int
        :param top: The top position of starting point on top left corner
        :type top: int
        :param keepScreen: Boolean to keep the generated file
        :type keepScreen: boolean
        :param getText: Boolean to try to getText from the capture
        :type getText: boolean

        :return: Eventually the text extract from the capture
        :rtype: string

        :Example:
        >>> takeScreenshot("Blizzard Battle.net", 300, 20, 370, 700, getText=True)
        Gameis mmllng.
        (Expected "Game is running")
    """
    # grab a handle to the main desktop window
    #hdesktop = win32gui.GetDesktopWindow()
    hdesktop = win32gui.FindWindow(None, windowName)

    ### Test to check if the Window exist
    try:
        rect = win32gui.GetWindowRect(hdesktop)
        print(rect)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        print(w, h, x, y)
    except:
        print("Impossible to FindWindow : " + windowName)
        exit()

    # some code to determine the size of all monitors in pixels
#    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
#    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
#    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
#    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # create a device context
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # create a memory based device context
    mem_dc = img_dc.CreateCompatibleDC()

    # create a bitmap object
    screenshot = win32ui.CreateBitmap()
    #screenshot.CreateCompatibleBitmap(img_dc, width, height)
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # copy the screen into our memory device context
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    ### Debug line
    #print(width, height, left, top, sep= ' ')

    # save the bitmap to a file
#    screenshot.SaveBitmapFile(mem_dc, 'C:\\Users\\François\\.spyder-py3\\screenshot.bmp')
    screenshot.SaveBitmapFile(mem_dc, 'screenshot.bmp')
    # free our objects
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    if getText:
        ### Paths must be adapated to be more robust
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = 'C:\\ProgramData\\Tesseract-OCR\\tesseract'
        TESSDATA_PREFIX= 'C:\\ProgramData\\Tesseract-OCR'
        tessdata_dir_config = '--tessdata-dir "C:\\ProgramData\\Tesseract-OCR\\tessdata"'
        from PIL import Image

        text = pytesseract.image_to_string(Image.open('screenshot.bmp'), lang='eng', config=tessdata_dir_config)
        print(text)

    if not keepScreen:
        os.remove('screenshot.bmp')

# some example
takeScreenshot("Blizzard Battle.net", 300, 20, 370, 700, getText=True)
