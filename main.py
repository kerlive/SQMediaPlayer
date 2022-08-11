from Qui.media_player import *
import sys
import UIresource_rc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Star()
    demo.show()
    
    sys.exit(app.exec_())