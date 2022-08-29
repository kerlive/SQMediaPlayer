from Qui.media_player import *
import sys
import UIresource_rc


if __name__ == '__main__':
    if len(sys.argv) == 2:
        media = sys.argv[1]
        app = QApplication(sys.argv)
        demo = Main()
        demo.show()
        demo.play_arg(media)

    else:

        app = QApplication(sys.argv)
        demo = Star()
        demo.show()


    sys.exit(app.exec_())