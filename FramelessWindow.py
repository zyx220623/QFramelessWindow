import sys
from PySide6.QtCore import (Qt,
                            QRect,
                            QSize,
                            QPoint)
from PySide6.QtGui import (QPixmap,
                           QMouseEvent,
                           QCursor,
                           QGuiApplication,
                           QIcon,
                           QFont, QAction)
from PySide6.QtWidgets import (QPushButton,
                               QWidget,
                               QApplication,
                               QMainWindow, QMenu)


class FrameLessWindow(QMainWindow):
    edge: int

    def __NoneEvent(self, event: QMouseEvent | None = None):
        pass

    def __attributeInit(self):
        self.movemode = 0
        self.is_mouse_pressed = False
        self.up_resized = False
        self.toDownPress = False
        self.left_resized = False
        self.toRightPress = False
        self.upleft_resized = False
        self.upright_resized = False
        self.downright_resized = False
        self.downleft_resized = False
        self.edge = 5
        self.beginning_pos_right = QCursor().pos()
        self.beginning_pos_up = QCursor().pos()
        self.beginning_pos_down = QCursor().pos()
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.__setWindowStatusMenu()
        self.__screen__ = QGuiApplication.primaryScreen().size()

    def __init__(self, parent: QWidget | None = None,
                 taskbar_height: int = 44,
                 MinimumSize: QSize = QSize(400, 225),
                 ReSize: QSize = QSize(400, 225),
                 Position: QPoint | None = None,
                 title_height: int = 35,
                 title_font_size: int = 15,
                 background_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (255, 255, 255, 1),
                 title_background_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (0, 0, 0, 1),
                 title_text_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (255, 255, 255, 1),
                 button_hoverColor: tuple[int, int, int, int] | list[int] | set[int] = (100, 100, 100, 1),
                 closeButton_hoverColor: tuple[int, int, int, int] | list[int] | set[int] = (255, 0, 0, 1)):
        super(FrameLessWindow, self).__init__(parent)
        self.__attributeInit()
        self.setMinimumSize(MinimumSize)
        self.resize(ReSize)
        self.taskbar_height = taskbar_height
        self.button_hoverColor = button_hoverColor
        self.closeButton_hoverColor = closeButton_hoverColor
        self.title_font_size = title_font_size
        self.parent_name = parent
        self.background_color_rgba = background_color_rgba
        self.title_background_color_rgba = title_background_color_rgba
        self.title_height = title_height
        self.title_text_color_rgba = title_text_color_rgba
        self.setStyleSheet("QMainWindow {"
                           f"background-color: rgba({background_color_rgba[0]},{background_color_rgba[1]},{background_color_rgba[2]},{background_color_rgba[3]});"
                           "border: none;"
                           "}")
        self.title = ""
        self.__setWindowTitleBar(background_color_rgba=self.title_background_color_rgba,
                                 color_rgba=self.title_text_color_rgba)
        self.__setMainWidget()
        self.__setThreeButton()
        if Position is not None:
            self.move(Position)
        else:
            self.move((self.__screen__.width() - self.size().width()) // 2,
                      (self.__screen__.height() - self.size().height() - self.taskbar_height) // 2)
        self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())

    def setWindowTitle(self, arg__1):
        super().setWindowTitle(arg__1)
        self.title = arg__1
        self.__setWindowTitleBar(background_color_rgba=self.title_background_color_rgba,
                                 color_rgba=self.title_text_color_rgba)

    def setWindowIcon(self, icon: QIcon | QPixmap):
        def windowIconDoubleClickedEvent(event: QMouseEvent):
            self.close()

        super().setWindowIcon(icon)
        self.__icon__ = icon
        self.icon_image = QPushButton(self)
        self.icon_image.setIcon(icon)
        self.icon_image.setIconSize(QSize(self.title_height - 10, self.title_height - 10))
        self.icon_image.setFixedSize(self.title_height - 10, self.title_height - 10)
        self.icon_image.move(5, 5)
        self.icon_image.setStyleSheet("QPushButton {"
                                      "background-color: rgba(0,0,0,0);"
                                      "border: none;"
                                      "}")
        self.icon_image.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.icon_image.customContextMenuRequested.connect(self.__showWindowStatusMenuFromIcon)
        self.icon_image.mouseDoubleClickEvent = windowIconDoubleClickedEvent

    def resizeEvent(self, event):
        self.WindowTitleBar.setGeometry(self.title_height + 5, 0, self.size().width(), self.title_height)
        self.MoveableArea.setGeometry(0, 0, self.size().width(), self.title_height)
        self.ToUpArea.setGeometry(0, 0, self.size().width(), self.edge)
        self.ToDownArea.setGeometry(0, self.size().height() - self.edge, self.size().width(), self.edge)
        self.ToLeftArea.setGeometry(0, 0, self.edge, self.size().height())
        self.ToRightArea.setGeometry(self.size().width() - self.edge, 0, self.edge, self.size().height())
        self.main_widget.setGeometry(0,
                                     self.title_height,
                                     self.size().width(),
                                     self.size().height())
        self.UpRightArea.setGeometry(self.size().width() - self.edge, 0, self.edge, self.edge)
        self.DownRightArea.setGeometry(self.size().width() - self.edge, self.size().height() - self.edge, self.edge,
                                       self.edge)
        self.DownLeftArea.setGeometry(0, self.size().height() - self.edge, self.edge,
                                      self.edge)
        self.CloseButton.move(self.size().width() - self.CloseButton.size().width(), 0)
        self.MaximumButton.move(self.CloseButton.pos().x() - self.MaximumButton.size().width(), 0)
        self.MinimumButton.move(self.MaximumButton.pos().x() - self.MinimumButton.size().width(), 0)
        self.CloseButton.raise_()
        self.MaximumButton.raise_()
        self.MinimumButton.raise_()
        self.ToUpArea.raise_()
        self.ToRightArea.raise_()
        self.ToDownArea.raise_()
        self.ToLeftArea.raise_()
        self.UpRightArea.raise_()
        self.DownRightArea.raise_()
        self.UpLeftArea.raise_()
        self.DownLeftArea.raise_()

    def close(self):
        super().close()

    def __setMainWidget(self):
        self.main_widget = QPushButton(self)
        self.main_widget.setStyleSheet("QPushButton {"
                                       "border: none;"
                                       f"background-color: rgba({self.background_color_rgba[0]}, {self.background_color_rgba[1]}, {self.background_color_rgba[2]}, 0);"
                                       "}")

    def __setNoneEvent(self):
        self.ToUpArea.mouseMoveEvent = self.__NoneEvent
        self.ToUpArea.mousePressEvent = self.__NoneEvent
        self.ToUpArea.mouseReleaseEvent = self.__NoneEvent
        self.ToDownArea.mouseMoveEvent = self.__NoneEvent
        self.ToDownArea.mousePressEvent = self.__NoneEvent
        self.ToDownArea.mouseReleaseEvent = self.__NoneEvent
        self.ToLeftArea.mouseMoveEvent = self.__NoneEvent
        self.ToLeftArea.mousePressEvent = self.__NoneEvent
        self.ToLeftArea.mouseReleaseEvent = self.__NoneEvent
        self.ToRightArea.mouseMoveEvent = self.__NoneEvent
        self.ToRightArea.mousePressEvent = self.__NoneEvent
        self.ToRightArea.mouseReleaseEvent = self.__NoneEvent
        self.UpLeftArea.mouseMoveEvent = self.__NoneEvent
        self.UpLeftArea.mousePressEvent = self.__NoneEvent
        self.UpLeftArea.mouseReleaseEvent = self.__NoneEvent
        self.UpRightArea.mouseMoveEvent = self.__NoneEvent
        self.UpRightArea.mousePressEvent = self.__NoneEvent
        self.UpRightArea.mouseReleaseEvent = self.__NoneEvent
        self.DownRightArea.mouseMoveEvent = self.__NoneEvent
        self.DownRightArea.mousePressEvent = self.__NoneEvent
        self.DownRightArea.mouseReleaseEvent = self.__NoneEvent
        self.DownLeftArea.mouseMoveEvent = self.__NoneEvent
        self.DownLeftArea.mousePressEvent = self.__NoneEvent
        self.DownLeftArea.mouseReleaseEvent = self.__NoneEvent
        self.__setWindowStatusMenuOnEdge()

    def __setNormalEvent(self):
        self.ToUpArea.mouseMoveEvent = self.__toUpMoveEvent
        self.ToUpArea.mousePressEvent = self.__toUpPressEvent
        self.ToUpArea.mouseReleaseEvent = self.__toUpReleaseEvent
        self.ToDownArea.mouseMoveEvent = self.__toDownMoveEvent
        self.ToDownArea.mousePressEvent = self.__toDownPressEvent
        self.ToDownArea.mouseReleaseEvent = self.__toDownReleaseEvent
        self.ToLeftArea.mouseMoveEvent = self.__toLeftMoveEvent
        self.ToLeftArea.mousePressEvent = self.__toLeftPressEvent
        self.ToLeftArea.mouseReleaseEvent = self.__toLeftReleaseEvent
        self.ToRightArea.mouseMoveEvent = self.__toRightMoveEvent
        self.ToRightArea.mousePressEvent = self.__toRightPressEvent
        self.ToRightArea.mouseReleaseEvent = self.__toRightReleaseEvent
        self.MoveableArea.mousePressEvent = self.__movePressEvent
        self.MoveableArea.mouseMoveEvent = self.__moveMoveEvent
        self.MoveableArea.mouseReleaseEvent = self.__moveReleaseEvent
        self.MoveableArea.mouseDoubleClickEvent = self.__titleDoubleClickedEvent
        self.UpLeftArea.mouseMoveEvent = self.__UpLeftMoveEvent
        self.UpLeftArea.mousePressEvent = self.__UpLeftPressEvent
        self.UpLeftArea.mouseReleaseEvent = self.__UpLeftReleaseEvent
        self.UpRightArea.mouseMoveEvent = self.__UpRightMoveEvent
        self.UpRightArea.mousePressEvent = self.__UpRightPressEvent
        self.UpRightArea.mouseReleaseEvent = self.__UpRightReleaseEvent
        self.DownRightArea.mouseMoveEvent = self.__DownRightMoveEvent
        self.DownRightArea.mousePressEvent = self.__DownRightPressEvent
        self.DownRightArea.mouseReleaseEvent = self.__DownRightReleaseEvent
        self.DownLeftArea.mouseMoveEvent = self.__DownLeftMoveEvent
        self.DownLeftArea.mousePressEvent = self.__DownLeftPressEvent
        self.DownLeftArea.mouseReleaseEvent = self.__DownLeftReleaseEvent
        self.__setWindowStatusMenu()

    def showMaximized(self):
        """自定义最大化方法"""
        super().showMaximized()
        self.MaximumButton.setIcon(QIcon("normal.png"))
        self.__setNoneEvent()
        self.__setWindowStatusMenuOnMax()

    def showLined(self):
        self.setGeometry(self.pos().x(), 0, self.size().width(), self.__screen__.height() - self.taskbar_height)
        self.__setNoneEvent()

    def showNormal(self):
        self.setGeometry(self.normal_geometry.x(), self.normal_geometry.y(), self.normal_geometry.width(),
                         self.normal_geometry.height())
        self.MaximumButton.setIcon(QIcon("max.png"))
        self.__setNormalEvent()
        if self.pos().y() <= 5 and self.__isLined() is not True:
            self.move(self.normal_geometry.x(), 5)

    def showSizeNormal(self):
        self.resize(self.normal_geometry.width(), self.normal_geometry.height())
        self.MaximumButton.setIcon(QIcon("max.png"))
        self.__setNormalEvent()

    def showUpLeft(self):
        self.setGeometry(0, 0, self.__screen__.width() // 2,
                         (self.__screen__.height() - self.taskbar_height) // 2)
        self.__setNoneEvent()

    def showFullLeft(self):
        self.setGeometry(0, 0, self.__screen__.width() // 2,
                         self.__screen__.height() - self.taskbar_height)
        self.__setNoneEvent()

    def showDownLeft(self):
        self.setGeometry(0, (self.__screen__.height() - self.taskbar_height) // 2,
                         self.__screen__.width() // 2,
                         (self.__screen__.height() - self.taskbar_height) // 2)
        self.__setNoneEvent()

    def showUpRight(self):
        self.setGeometry(self.__screen__.width() // 2, 0,
                         self.__screen__.width() // 2,
                         (self.__screen__.height() - self.taskbar_height) // 2)
        self.__setNoneEvent()

    def showDownRight(self):
        self.setGeometry(self.__screen__.width() // 2,
                         (self.__screen__.height() - self.taskbar_height) // 2,
                         self.__screen__.width() // 2,
                         (self.__screen__.height() - self.taskbar_height) // 2)
        self.__setNoneEvent()

    def showFullRight(self):
        self.setGeometry(self.__screen__.width() // 2, 0,
                         self.__screen__.width() // 2,
                         self.__screen__.height() - self.taskbar_height)
        self.__setNoneEvent()

    def isMaximized(self) -> bool:
        """自定义最大化规则"""
        return super().isMaximized()

    def __isLined(self) -> bool:
        if self.size().height() == self.__screen__.height() - self.taskbar_height and self.pos().y() == 0:
            return True
        else:
            return False

    def __isFullSide(self) -> bool:
        if self.size().width() == self.__screen__.width() // 2 and \
                self.size().height() == self.__screen__.height() - self.taskbar_height and \
                self.pos().y() == 0:
            if self.pos().x() == self.__screen__.width() // 2 or \
                    self.pos().x() == 0:
                return True
            else:
                return False
        else:
            return False

    def __isFullCorner(self) -> bool:
        result = True
        if (self.size().width() != self.__screen__.width() // 2 or self.size().height() != (
                self.__screen__.height() - self.taskbar_height) // 2) and \
                (self.pos().x() <= 5 or self.pos().x() != self.__screen__.width() // 2) and \
                (self.pos().y() <= 5 or self.pos().y() != (self.__screen__.height() - self.taskbar_height) // 2):
            result = False
        return result

    def __titleDoubleClickedEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isMaximized() or self.__isLined() or self.__isFullCorner() or self.__isFullSide():
                self.showNormal()
            else:
                self.showMaximized()

    def __setWindowTitleBar(self,
                            background_color_rgba: tuple[int, int, int, int] | list[int] | set[int],
                            color_rgba: tuple[int, int, int, int] | list[int] | set[int]):
        try:
            self.title
        except:
            self.title = ""
        self.WindowTitleBackground = QPushButton(self)
        self.WindowTitleBackground.setStyleSheet("QPushButton {"
                                                 f"background-color: rgba({background_color_rgba[0]}, {background_color_rgba[1]}, {background_color_rgba[2]}, {background_color_rgba[3]});"
                                                 "border: none;"
                                                 "}")
        self.WindowTitleBackground.setGeometry(0, 0, self.__screen__.width(), self.title_height)
        self.WindowTitleBar = QPushButton(self.title, self)
        self.WindowTitleBar.setGeometry(self.title_height + 5, 0, self.size().width(), self.title_height)
        self.WindowTitleBar.setStyleSheet("QPushButton {"
                                          "text-align: left;"
                                          f'font: normal normal {self.title_font_size}px "微软雅黑";'
                                          f"background-color: rgba(0,0,0,0);"
                                          f"color: rgba({color_rgba[0]}, {color_rgba[1]}, {color_rgba[2]}, {color_rgba[3]});"
                                          "border: none;"
                                          "}")
        self.__setMoveableArea()

    def __setWindowStatusMenu(self):
        self.WindowStatusMenu = QMenu(self)
        self.WindowStatusMenu_qss = ("QMenu {"
                                     "background-color:rgb(40, 40, 40);"
                                     "color:rgb(255, 255, 255);"
                                     "border: 1px solid rgb(127, 127, 127);"
                                     "}"
                                     "QMenu:item:selected {"
                                     "background-color:rgb(80, 80, 80);"
                                     "}"
                                     "QMenu:separator{"
                                     "height:1px;"
                                     "background-color:rgba(123,123,123,1);"
                                     "margin-left:22px;"
                                     "margin-right:1px;"
                                     "}"
                                     "QMenu:item:disabled {"
                                     "color:rgb(100,100,100);"
                                     "background-color:rgb(40, 40, 40);"
                                     "}")
        self.WindowStatusMenu.setStyleSheet(self.WindowStatusMenu_qss)
        self.NormalAction = QAction("还原(&R)", self)
        self.NormalAction.setEnabled(False)
        self.NormalAction.triggered.connect(self.showNormal)
        self.NormalAction.setIcon(QIcon("normalborder.png"))
        self.WindowStatusMenu.addAction(self.NormalAction)
        self.MoveAction = QAction("移动(&M)", self)
        self.WindowStatusMenu.addAction(self.MoveAction)
        self.SizeAction = QAction("大小(&S)", self)
        self.WindowStatusMenu.addAction(self.SizeAction)
        self.MinAction = QAction("最小化(&N)", self)
        self.MinAction.setIcon(QIcon("minborder.png"))
        self.MinAction.triggered.connect(self.showMinimized)
        self.WindowStatusMenu.addAction(self.MinAction)
        self.MaxAction = QAction("最大化(&X)", self)
        self.MaxAction.triggered.connect(self.showMaximized)
        self.MaxAction.setIcon(QIcon("maxborder.png"))
        self.WindowStatusMenu.addAction(self.MaxAction)
        self.WindowStatusMenu.addSeparator()
        self.CloseAction = QAction("关闭(&C)", self)
        self.CloseAction.setShortcut("Alt+F4")
        self.CloseAction.setIcon(QIcon("closeborder.png"))
        self.CloseAction.triggered.connect(self.close)
        self.WindowStatusMenu.addAction(self.CloseAction)

    def __setWindowStatusMenuOnEdge(self):
        self.WindowStatusMenu = QMenu(self)
        self.WindowStatusMenu.setStyleSheet(self.WindowStatusMenu_qss)
        self.NormalAction = QAction("还原(&R)", self)
        self.NormalAction.triggered.connect(self.showNormal)
        self.NormalAction.setIcon(QIcon("normalborder.png"))
        self.WindowStatusMenu.addAction(self.NormalAction)
        self.MoveAction = QAction("移动(&M)", self)
        self.WindowStatusMenu.addAction(self.MoveAction)
        self.SizeAction = QAction("大小(&S)", self)
        self.SizeAction.setEnabled(False)
        self.WindowStatusMenu.addAction(self.SizeAction)
        self.MinAction = QAction("最小化(&N)", self)
        self.MinAction.setIcon(QIcon("minborder.png"))
        self.MinAction.triggered.connect(self.showMinimized)
        self.WindowStatusMenu.addAction(self.MinAction)
        self.MaxAction = QAction("最大化(&X)", self)
        self.MaxAction.triggered.connect(self.showMaximized)
        self.MaxAction.setIcon(QIcon("maxborder.png"))
        self.WindowStatusMenu.addAction(self.MaxAction)
        self.WindowStatusMenu.addSeparator()
        self.CloseAction = QAction("关闭(&C)", self)
        self.CloseAction.setShortcut("Alt+F4")
        self.CloseAction.setIcon(QIcon("closeborder.png"))
        self.CloseAction.triggered.connect(self.close)
        self.WindowStatusMenu.addAction(self.CloseAction)

    def __setWindowStatusMenuOnMax(self):
        self.WindowStatusMenu = QMenu(self)
        self.WindowStatusMenu.setStyleSheet(self.WindowStatusMenu_qss)
        self.NormalAction = QAction("还原(&R)", self)
        self.NormalAction.triggered.connect(self.showNormal)
        self.NormalAction.setIcon(QIcon("normalborder.png"))
        self.WindowStatusMenu.addAction(self.NormalAction)
        self.MoveAction = QAction("移动(&M)", self)
        self.WindowStatusMenu.addAction(self.MoveAction)
        self.SizeAction = QAction("大小(&S)", self)
        self.SizeAction.setEnabled(False)
        self.WindowStatusMenu.addAction(self.SizeAction)
        self.MinAction = QAction("最小化(&N)", self)
        self.MinAction.setIcon(QIcon("minborder.png"))
        self.MinAction.triggered.connect(self.showMinimized)
        self.WindowStatusMenu.addAction(self.MinAction)
        self.MaxAction = QAction("最大化(&X)", self)
        self.MaxAction.setEnabled(False)
        self.MaxAction.triggered.connect(self.showMaximized)
        self.MaxAction.setIcon(QIcon("maxborder.png"))
        self.WindowStatusMenu.addAction(self.MaxAction)
        self.WindowStatusMenu.addSeparator()
        self.CloseAction = QAction("关闭(&C)", self)
        self.CloseAction.setShortcut("Alt+F4")
        self.CloseAction.setIcon(QIcon("closeborder.png"))
        self.CloseAction.triggered.connect(self.close)
        self.WindowStatusMenu.addAction(self.CloseAction)

    def __showWindowStatusMenuFromTitle(self, pos: QPoint):
        self.WindowStatusMenu.exec(self.MoveableArea.mapToGlobal(pos))

    def __showWindowStatusMenuFromIcon(self, pos: QPoint):
        self.WindowStatusMenu.exec(self.icon_image.mapToGlobal(pos))

    def __setMinimumButton(self):
        self.MinimumButton = QPushButton(self)
        self.MinimumButton.setIcon(QIcon("min.png"))
        self.MinimumButton.setIconSize(QSize(self.title_height - 20, self.title_height - 20))
        self.MinimumButton.setStyleSheet("QPushButton {"
                                         "background-color: rgba(25, 25, 25, 0);"
                                         "border: none;"
                                         "}"
                                         "QPushButton:hover {"
                                         f"background-color: rgba({self.button_hoverColor[0]},{self.button_hoverColor[1]},{self.button_hoverColor[2]}, {self.button_hoverColor[3]});"
                                         "}")
        self.MinimumButton.resize(self.title_height, self.title_height)
        self.MinimumButton.move(self.MaximumButton.pos().x() - self.MinimumButton.size().width(), 0)
        self.MinimumButton.clicked.connect(self.showMinimized)

    def __setMaximumButton(self):
        self.MaximumButton = QPushButton(self)
        self.MaximumButton.setIcon(QIcon("max.png"))
        self.MaximumButton.setIconSize(QSize(self.title_height - 20, self.title_height - 20))
        self.MaximumButton.resize(self.title_height, self.title_height)
        self.MaximumButton.setStyleSheet("QPushButton {"
                                         "background-color: rgba(25, 25, 25, 0);"
                                         "color: rgba(255,255,255,1);"
                                         "border: none;"
                                         "}"
                                         "QPushButton:hover {"
                                         f"background-color: rgba({self.button_hoverColor[0]},{self.button_hoverColor[1]},{self.button_hoverColor[2]}, {self.button_hoverColor[3]});"
                                         "color: rgba(255,255,255,1);"
                                         "}")
        self.MaximumButton.move(self.CloseButton.pos().x() - self.MaximumButton.size().width(), 0)
        self.MaximumButton.clicked.connect(self.MaximumButtonClickedEvent)

    def __setCloseButton(self):
        self.CloseButton = QPushButton(self)
        self.CloseButton.resize(self.title_height, self.title_height)
        self.CloseButton.setIcon(QIcon("close.png"))
        self.CloseButton.setIconSize(QSize(self.title_height - 20, self.title_height - 20))
        self.CloseButton.setStyleSheet("QPushButton {"
                                       "background-color: rgba(25, 25, 25, 0);"
                                       "color: rgba(255,255,255,1);"
                                       "border: none;"
                                       "}"
                                       "QPushButton:hover {"
                                       f"background-color: rgba({self.closeButton_hoverColor[0]},{self.closeButton_hoverColor[1]},{self.closeButton_hoverColor[2]}, {self.closeButton_hoverColor[3]});"
                                       "color: rgba(255,255,255,1);"
                                       "}")
        self.CloseButton.move(self.size().width() - self.CloseButton.size().width(), 0)
        self.CloseButton.raise_()
        self.CloseButton.clicked.connect(self.close)

    def __setThreeButton(self):
        self.__setCloseButton()
        self.__setMaximumButton()
        self.__setMinimumButton()

    def MaximumButtonClickedEvent(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def __setMoveableArea(self):
        self.MoveableArea = QPushButton(self)
        self.MoveableArea.setStyleSheet("QPushButton {"
                                        "background-color: rgba(255,255,255,0);"
                                        "border: none;"
                                        "}")
        self.MoveableArea.setGeometry(0, 0, self.size().width(), self.title_height)
        self.MoveableArea.mousePressEvent = self.__movePressEvent
        self.MoveableArea.mouseMoveEvent = self.__moveMoveEvent
        self.MoveableArea.mouseReleaseEvent = self.__moveReleaseEvent
        self.MoveableArea.mouseDoubleClickEvent = self.__titleDoubleClickedEvent
        self.MoveableArea.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.MoveableArea.customContextMenuRequested.connect(self.__showWindowStatusMenuFromTitle)
        self.__setToUpArea()

    def __setToUpArea(self):
        self.ToUpArea = QPushButton(self.MoveableArea)
        self.ToUpArea.setStyleSheet("QPushButton {"
                                    "background-color: rgba(255,255,255,0);"
                                    "border: none;"
                                    "}")
        self.ToUpArea.setGeometry(0, 0, self.size().width(), self.edge)
        self.ToUpArea.setCursor(Qt.CursorShape.SizeVerCursor)
        self.ToUpArea.mouseMoveEvent = self.__toUpMoveEvent
        self.ToUpArea.mousePressEvent = self.__toUpPressEvent
        self.ToUpArea.mouseReleaseEvent = self.__toUpReleaseEvent
        self.__setToDownArea()

    def __setToDownArea(self):
        self.ToDownArea = QPushButton(self)
        self.ToDownArea.setStyleSheet("QPushButton {"
                                      "background-color: rgba(255,255,255,0);"
                                      "border: none;"
                                      "}")
        self.ToDownArea.setGeometry(0, self.size().height() - self.edge, self.size().width(), self.edge)
        self.ToDownArea.setCursor(Qt.CursorShape.SizeVerCursor)
        self.ToDownArea.mouseMoveEvent = self.__toDownMoveEvent
        self.ToDownArea.mousePressEvent = self.__toDownPressEvent
        self.ToDownArea.mouseReleaseEvent = self.__toDownReleaseEvent
        self.__setToLeftArea()

    def __setToLeftArea(self):
        self.ToLeftArea = QPushButton(self)
        self.ToLeftArea.setStyleSheet("QPushButton {"
                                      "background-color: rgba(255,255,255,0);"
                                      "border: none;"
                                      "}")
        self.ToLeftArea.setGeometry(0, 0, self.edge, self.size().height())
        self.ToLeftArea.setCursor(Qt.CursorShape.SizeHorCursor)
        self.ToLeftArea.mouseMoveEvent = self.__toLeftMoveEvent
        self.ToLeftArea.mousePressEvent = self.__toLeftPressEvent
        self.ToLeftArea.mouseReleaseEvent = self.__toLeftReleaseEvent
        self.__setToRightArea()

    def __setToRightArea(self):
        self.ToRightArea = QPushButton(self)
        self.ToRightArea.setStyleSheet("QPushButton {"
                                       "background-color: rgba(255,255,255,0);"
                                       "border: none;"
                                       "}")
        self.ToRightArea.setGeometry(self.size().width() - self.edge, 0, self.edge, self.size().height())
        self.ToRightArea.setCursor(Qt.CursorShape.SizeHorCursor)
        self.ToRightArea.mouseMoveEvent = self.__toRightMoveEvent
        self.ToRightArea.mousePressEvent = self.__toRightPressEvent
        self.ToRightArea.mouseReleaseEvent = self.__toRightReleaseEvent
        self.__setUpLeftArea()

    def __toRightPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.right_click_position = event.globalPosition().toPoint() - self.pos()
            self.beginning_pos_x = QCursor.pos().x()
            self.toRightPress = True
            self._width_ = self.size().width()

    def __toRightMoveEvent(self, event: QMouseEvent):
        if self.toRightPress and QCursor.pos().x() >= self.pos().x() + self.minimumWidth() - self.edge:
            self.resize(self._width_ + (QCursor.pos().x() - self.beginning_pos_x), self.size().height())
        event.accept()

    def __toRightReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toRightPress = False
            self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __movePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and \
                event.position().y() <= self.title_height:
            self.is_mouse_pressed = True
            self.mouse_click_position = event.globalPosition().toPoint() - self.pos()
            if self.isMaximized():
                self.movemode = 1
            elif self.__isFullSide():
                self.movemode = 3
            elif self.__isFullCorner():
                self.movemode = 4
            elif self.__isLined():
                self.movemode = 2
            else:
                self.movemode = 0
        event.accept()

    def __moveMoveEvent(self, event: QMouseEvent):
        if self.is_mouse_pressed:
            if self.movemode == 0:
                self.move(event.globalPosition().toPoint() - self.mouse_click_position)
            elif self.movemode == 3:
                self.showSizeNormal()
                self.move(
                    event.globalPosition().toPoint().x() - self.mouse_click_position.x() * self.normal_geometry.width() // (
                            self.__screen__.width() // 2),
                    (event.globalPosition().toPoint() - self.mouse_click_position).y())
            elif self.movemode == 1:
                self.showSizeNormal()
                self.move(
                    event.globalPosition().toPoint().x() - self.mouse_click_position.x() * self.normal_geometry.width() // QGuiApplication.primaryScreen().geometry().width(),
                    (event.globalPosition().toPoint() - self.mouse_click_position).y())
            elif self.movemode == 4:
                self.showSizeNormal()
                self.move(
                    event.globalPosition().toPoint().x() - self.mouse_click_position.x() * self.normal_geometry.width() // (
                            self.__screen__.width() // 2),
                    (event.globalPosition().toPoint() - self.mouse_click_position).y())
            elif self.movemode == 2:
                self.showSizeNormal()
                self.move(event.globalPosition().toPoint() - self.mouse_click_position)

        event.accept()

    def __moveReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_mouse_pressed = False
            if QCursor.pos().y() <= 0 and self.__screen__.width() - 5 > QCursor.pos().x() > 5:
                self.showMaximized()
            elif QCursor.pos().x() <= 5 and QCursor.pos().y() <= 5:
                self.showUpLeft()
            elif QCursor.pos().x() >= self.__screen__.width() - 5 and QCursor.pos().y() <= 5:
                self.showUpRight()
            elif QCursor.pos().x() <= 5 and QCursor.pos().y() >= self.__screen__.height() - self.taskbar_height:
                self.showDownLeft()
            elif QCursor.pos().y() >= self.__screen__.height() - self.taskbar_height and \
                    QCursor.pos().x() >= self.__screen__.width() - 5:
                self.showDownRight()
            elif QCursor.pos().x() <= 5 <= QCursor.pos().y() <= self.__screen__.height() - 5:
                self.showFullLeft()
            elif QCursor.pos().x() >= self.__screen__.width() - 5 and \
                    self.__screen__.height() - 5 >= QCursor.pos().y() >= 5:
                self.showFullRight()
            elif QCursor.pos().y() >= self.__screen__.height() - self.taskbar_height and 5 <= QCursor.pos().x() <= self.__screen__.width() - 5:
                self.setGeometry(self.normal_geometry.x(), self.normal_geometry.y(), self.normal_geometry.width(),
                                 self.normal_geometry.height())
            elif not (self.isMaximized() or self.__isLined() or self.__isFullSide() or self.__isFullCorner()):
                self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __toUpPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and \
                event.position().y() <= self.edge:
            self.up_resized = True
            self.up_click_position = event.globalPosition().toPoint() - self.pos()
            self._x_ = self.pos().x()
            self._y_ = self.pos().y()
            self._width_ = self.size().width()
            self._height_ = self.size().height()
            self.beginning_pos_y = QCursor().pos().y()
            self.justnow_size_list = []
        event.accept()

    def __toUpMoveEvent(self, event: QMouseEvent):
        if self.up_resized and self.size().height() + self.pos().y() - QCursor.pos().y() >= self.minimumHeight():
            self.resize(self._width_, self._height_ - QCursor.pos().y() + self.beginning_pos_y)
            self.move(self._x_, (event.globalPosition().toPoint() - self.up_click_position).y())
        event.accept()

    def __toUpReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.up_resized = False
            if QCursor.pos().y() <= 0 and QGuiApplication.primaryScreen().geometry().width() - 5 > QCursor.pos().x() > 5:
                self.showLined()
            else:
                self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __toDownPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.down_click_position = event.globalPosition().toPoint() - self.pos()
            self.beginning_pos_y = QCursor.pos().y()
            self._height_ = self.size().height()
            self.toDownPress = True

    def __toDownMoveEvent(self, event: QMouseEvent):
        if self.toDownPress and QCursor.pos().y() >= self.minimumHeight() + self.pos().y():
            self.resize(self.size().width(), self._height_ + (QCursor.pos().y() - self.beginning_pos_y))
        event.accept()

    def __toDownReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toDownPress = False
            if QCursor.pos().y() >= self.__screen__.height() - self.taskbar_height and \
                    5 <= QCursor.pos().x() <= self.__screen__.width() - self.edge:
                self.showLined()
            else:
                self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __toLeftPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and \
                event.position().x() <= self.edge:
            self.left_resized = True
            self.left_click_position = event.globalPosition().toPoint() - self.pos()
            self._x_ = self.pos().x()
            self._y_ = self.pos().y()
            self._width_ = self.size().width()
            self._height_ = self.size().height()
            self.beginning_pos_x = QCursor().pos().x()
        event.accept()

    def __toLeftMoveEvent(self, event: QMouseEvent):
        if self.left_resized and self.pos().x() + self.size().width() - QCursor.pos().x() >= self.minimumWidth():
            self.resize(self._width_ - QCursor.pos().x() + self.beginning_pos_x, self.height())
            self.move((event.globalPosition().toPoint() - self.left_click_position).x(), self._y_)
        event.accept()

    def __toLeftReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_resized = False
            self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __setUpLeftArea(self):
        self.UpLeftArea = QPushButton(self)
        self.UpLeftArea.setStyleSheet("QPushButton {"
                                      "background-color: rgba(255,255,255,0);"
                                      "border: none;"
                                      "}")
        self.UpLeftArea.setGeometry(0, 0, self.edge, self.edge)
        self.UpLeftArea.setCursor(Qt.CursorShape.SizeFDiagCursor)
        self.UpLeftArea.mouseMoveEvent = self.__UpLeftMoveEvent
        self.UpLeftArea.mousePressEvent = self.__UpLeftPressEvent
        self.UpLeftArea.mouseReleaseEvent = self.__UpLeftReleaseEvent
        self.__setUpRightArea()

    def __UpLeftPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.upleft_resized = True
            self.upleft_click_position = event.globalPosition().toPoint() - self.pos()
            self._x_ = self.pos().x()
            self._y_ = self.pos().y()
            self._width_ = self.size().width()
            self._height_ = self.size().height()
            self.beginning_pos = QCursor().pos()
        event.accept()

    def __UpLeftMoveEvent(self, event: QMouseEvent):
        if self.upleft_resized and \
                self.pos().x() + self.size().width() - QCursor.pos().x() >= self.minimumWidth():
            self.resize(self._width_ - QCursor.pos().x() + self.beginning_pos.x(),
                        self.size().height())
            self.move((event.globalPosition().toPoint() - self.upleft_click_position).x(), self.pos().y())
        if self.upleft_resized and \
                self.pos().y() + self.size().height() - QCursor.pos().y() >= self.minimumHeight():
            self.resize(self.size().width(),
                        self._height_ - QCursor.pos().y() + self.beginning_pos.y())
            self.move(self.pos().x(), (event.globalPosition().toPoint() - self.upleft_click_position).y())
        event.accept()

    def __UpLeftReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.upleft_resized = False
            self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __setUpRightArea(self):
        self.UpRightArea = QPushButton(self)
        self.UpRightArea.setStyleSheet("QPushButton {"
                                       "background-color: rgba(255,255,255,0);"
                                       "border: none;"
                                       "}")
        self.UpRightArea.setGeometry(self.size().width() - self.edge, 0, self.edge, self.edge)
        self.UpRightArea.setCursor(Qt.CursorShape.SizeBDiagCursor)
        self.UpRightArea.mouseMoveEvent = self.__UpRightMoveEvent
        self.UpRightArea.mousePressEvent = self.__UpRightPressEvent
        self.UpRightArea.mouseReleaseEvent = self.__UpRightReleaseEvent
        self.__setDownRightArea()

    def __UpRightPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.upright_resized = True
            self.upleft_click_position = event.globalPosition().toPoint() - self.pos()
            self._x_ = self.pos().x()
            self._y_ = self.pos().y()
            self._width_ = self.size().width()
            self._height_ = self.size().height()
            self.beginning_pos_right = QCursor().pos()
            self.beginning_pos_up = QCursor().pos()
        event.accept()

    def __UpRightMoveEvent(self, event: QMouseEvent):
        if self.upright_resized and QCursor.pos().x() >= self.pos().x() + self.minimumWidth() - self.edge:
            self.resize(self._width_ + (QCursor.pos().x() - self.beginning_pos_right.x()), self.size().height())
        if self.upright_resized and self.pos().y() + self.size().height() - QCursor.pos().y() >= self.minimumHeight():
            self.resize(self.width(), self._height_ - QCursor.pos().y() + self.beginning_pos_up.y())
            self.move(self._x_, (event.globalPosition().toPoint() - self.upleft_click_position).y())
        event.accept()

    def __UpRightReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.upright_resized = False
            self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __setDownRightArea(self):
        self.DownRightArea = QPushButton(self)
        self.DownRightArea.setStyleSheet("QPushButton {"
                                         "background-color: rgba(255,255,255,0);"
                                         "border: none;"
                                         "}")
        self.DownRightArea.setGeometry(self.size().width() - self.edge, self.size().height() - self.edge, self.edge,
                                       self.edge)
        self.DownRightArea.setCursor(Qt.CursorShape.SizeFDiagCursor)
        self.DownRightArea.mouseMoveEvent = self.__DownRightMoveEvent
        self.DownRightArea.mousePressEvent = self.__DownRightPressEvent
        self.DownRightArea.mouseReleaseEvent = self.__DownRightReleaseEvent
        self.__setDownLeftArea()

    def __DownRightPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.downright_resized = True
            self.upleft_click_position = event.globalPosition().toPoint() - self.pos()
            self._x_ = self.pos().x()
            self._y_ = self.pos().y()
            self._width_ = self.size().width()
            self._height_ = self.size().height()
            self.beginning_pos_right = QCursor().pos()
            self.beginning_pos_down = QCursor().pos()
        event.accept()

    def __DownRightMoveEvent(self, event: QMouseEvent):
        if self.downright_resized and (
                event.globalPosition().toPoint() - self.pos()).y() >= self.minimumHeight() - self.edge:
            self.resize(self.size().width(), self._height_ + (QCursor.pos().y() - self.beginning_pos_down.y()))
        if self.downright_resized and QCursor.pos().x() >= self.pos().x() + self.minimumWidth() - self.edge:
            self.resize(self._width_ + (QCursor.pos().x() - self.beginning_pos_right.x()), self.size().height())
        event.accept()

    def __DownRightReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.downright_resized = False
            self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()

    def __setDownLeftArea(self):
        self.DownLeftArea = QPushButton(self)
        self.DownLeftArea.setStyleSheet("QPushButton {"
                                        "background-color: rgba(255,255,255,0);"
                                        "border: none;"
                                        "}")
        self.DownLeftArea.setGeometry(0, self.size().height() - self.edge, self.edge,
                                      self.edge)
        self.DownLeftArea.setCursor(Qt.CursorShape.SizeBDiagCursor)
        self.DownLeftArea.mouseMoveEvent = self.__DownLeftMoveEvent
        self.DownLeftArea.mousePressEvent = self.__DownLeftPressEvent
        self.DownLeftArea.mouseReleaseEvent = self.__DownLeftReleaseEvent

    def __DownLeftPressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.downleft_resized = True
            self.upleft_click_position = event.globalPosition().toPoint() - self.pos()
            self._x_ = self.pos().x()
            self._y_ = self.pos().y()
            self._width_ = self.size().width()
            self._height_ = self.size().height()
            self.beginning_pos_left = QCursor().pos()
            self.beginning_pos_down = QCursor().pos()
        event.accept()

    def __DownLeftMoveEvent(self, event: QMouseEvent):
        if self.downleft_resized and (
                event.globalPosition().toPoint() - self.pos()).y() >= self.minimumHeight() - self.edge:
            self.resize(self.size().width(), self._height_ + (QCursor.pos().y() - self.beginning_pos_down.y()))
        if self.downleft_resized and self.pos().x() + self.size().width() - QCursor.pos().x() >= self.minimumWidth():
            self.resize(self._width_ - QCursor.pos().x() + self.beginning_pos_left.x(), self.size().height())
            self.move((event.globalPosition().toPoint() - self.upleft_click_position).x(), self._y_)
        event.accept()

    def __DownLeftReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.downleft_resized = False
            self.normal_geometry = QRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().height())
        event.accept()


app = QApplication(sys.argv)
window = FrameLessWindow(taskbar_height=40,
                         title_height=35,
                         title_font_size=15,
                         MinimumSize=QSize(800, 450))
window.setWindowTitle("FramelessWindow 示例")
window.setWindowIcon(QIcon("icon.png"))  # 替换成你的图标路径
window.show()
app.exec()
