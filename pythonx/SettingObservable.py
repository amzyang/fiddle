# coding: utf-8
class SettingObservable(object):
    changed = False
    observers = []

    def notifyObservers(self):
        if (self.changed):
            for observer in self.observers:
                observer.update(self)
        self.changed = False

    def addObserver(self, observer):
        self.observers.append(observer)

    def setChanged(self):
        self.changed = True

    def settingUpdated(self):
        self.setChanged()
        self.notifyObservers()


# vim: cursorcolumn tabstop=4 expandtab shiftwidth=4 softtabstop=4 textwidth=79
