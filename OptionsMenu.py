from GuiScene import *
import clipboard

class OptionsMenu(GuiScene):
    def init(self, **params):
        super().init()
        # size = [50, 50]
        # self.buttons = []

        # for x in range(6):
        #     for y in reversed(range(8)):
                # self.buttons.append(CheckBox([(x * size[0]) + 5, (y * size[1]) + 5], self.uiManager, '', size=size, dragable=True))

        # buttonSize = [120, 40]

        self.elements += (
            # Button([200 - buttonSize[0], 410], self.uiManager, 'Generate Hex', self.generateHex, size=buttonSize),
            InputBox([50, 50], self.uiManager, 'Frames per Generation', '200', True),
        )


    # def generateHex(self):
    #     # print('gen hex called!')
    #     # for i in self.buttons:
    #     #     print(i.checked)
    #     # return ''
    #     allVals   = []
    #     columnVal = ''
    #     for cnt, x in enumerate(self.buttons):
    #         columnVal += '1' if x.checked else '0'
    #         if (cnt + 1) % 8 == 0:
    #             print('columnVal:', columnVal)
    #             allVals.append(int(copy.deepcopy(columnVal), 2))
    #             columnVal = ''

    #     print('allVals:', allVals)

    #     returnString = '{'
    #     for i in allVals:
    #         returnString += f"{i:#0{4}x}, "
    #     returnString = returnString[:-2]
    #     returnString += '}, // '

    #     clipboard.copy(returnString)
    #     print(returnString)

    #     def keyDown(self, event):
    #         key = super().keyDown(event)
            
    #         if key == 'escape':
    #             self.exit()
    #         if key == 'enter' or key == 'return':
    #             self.generateHex()
    #         if key == 'c' or key == 'r':
    #             for i in self.buttons:
    #                 i.checked = False
    #                 i.rebuild()

    # def mouseLeftButtonDown(self):
    #     self.mouseHeld = True

    # def mouseLeftButtonUp(self):
    #     self.mouseHeld = False

    # def handleOtherEvent(self, event):
    #     for i in self.buttons:
    #         i.handleEvent(event, mouseHeld=self.mouseHeld)