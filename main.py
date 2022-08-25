from Qui.media_player import *
import sys
import UIresource_rc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Star()
    demo.show()
    
    if len(sys.argv) != 1:
        media = []
        for i in range(len(sys.argv)):
            media += sys.argv[i]
        print("play meida")

    sys.exit(app.exec_())