import os
import win32gui, win32ui, win32con

from .MyRect import MyRect
import pytesseract

def reCalculateScreenShotRect(sShotRect, winRect):
    return sShotRect

def takeScreenshot(windowName, sShotRect, toFileName, keepScreen=True):
    """
        This function allow to take screenshot of a specific window designate
        by is name, you must also specify, the starting point (left, top) and
        the size (width, height) of the zone you want to extractself.
        Then you can decide to keep or not the generated file and choose to try
        to evaluate a text from this file with pytesseract prebuild method.

        :param windowName: The name of the window
        :type windowName: string
        :param rect: The rect where to take the shot
        :type rect: QRect
        :param keepScreen: Boolean to keep the generated file
        :type keepScreen: boolean
        :param toFileName: the fileName where the screenShot is saved
        :type toFileName : string
        :return: Eventually the text extract from the capture
        :rtype: string

        :Example:
        >>> takeScreenshot("Blizzard Battle.net", QRect(300, 20, 370, 700), getText=True)
        Gameis mmllng.
        (Expected "Game is running")
    """
    # grab a handle to the main desktop window
    #hdesktop = win32gui.GetDesktopWindow()
    hdesktop = win32gui.FindWindow(None, windowName)
    winRect= MyRect.fromWindow(hdesktop)
    reCalcRect = reCalculateScreenShotRect(sShotRect ,winRect)


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
    screenshot.CreateCompatibleBitmap(img_dc, reCalcRect.width(), reCalcRect.height())
    mem_dc.SelectObject(screenshot)

    # copy the screen into our memory device context
    mem_dc.BitBlt((0, 0), reCalcRect.widthHeightTuple(), img_dc, reCalcRect.leftTopTuple(), win32con.SRCCOPY)

    # save the bitmap to a file
#    screenshot.SaveBitmapFile(mem_dc, 'C:\\Users\\François\\.spyder-py3\\screenshot.bmp')
    screenshot.SaveBitmapFile(mem_dc, toFileName)
    # free our objects
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    print("Screenshot taken")
    if not keepScreen:
        os.remove('screenshot.bmp')

def findTextInImage(fileName):
    ### Paths must be adapated to be more robust

    from PIL import Image
    from MainWindow import tessdata_dir_config
    text = pytesseract.image_to_string(Image.open(fileName), lang='eng', config=tessdata_dir_config)
    print(text)
    return text
