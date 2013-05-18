# coding=utf-8
import sublime
import sublime_plugin
import datetime
import time
import subprocess
import os


class AlarmClockCommand(sublime_plugin.TextCommand):

    alarmSettingFile = "AlarmClock.sublime-settings"
    storageFormat = "%a %b %d %H:%M:%S %Y"
    displayFormat = "%a %b %d %H:%M:%S"
    snoozeTimeMins = 9
    settings = False

    def run(self, edit, action=None, alarmId=None):
        action = str(action).lower()

        if action == "none" or action == "choose":
            self.choose()
        if action == "new_alarm":
            self.new()
        elif action == "edit_alarm":
            self.edit(alarmId)
        elif action == "list_alarms":
            self.list(alarmId)
        elif action == "enable_alarm":
            self.enable(alarmId)
        elif action == "enable_all_alarms":
            self.enableAll()
        elif action == "disable_alarm":
            self.disable(alarmId)
        elif action == "disable_all_alarms":
            self.disableAll()
        elif action == "delete_alarm":
            self.delete(alarmId)
        elif action == "delete_all_alarms":
            self.deleteAll()
        elif action == "on_app_start":
            self.onAppStart()
        else:
            return sublime.status_message(
                "Unknown action \"%s\"." % action
            )

    def choose(self):
        items = [
            "New alarm",
            "Edit alarm",
            "List alarms",
            "Enable alarm",
            "Enable all alarms",
            "Disable alarm",
            "Disable all alarms",
            "Delete alarm",
            "Delete all alarms"
        ]
        self.show_quick_panel(items, self.chooseType)

    def chooseType(self, selection):
        if selection == 0:
            self.new()
        elif selection == 1:
            self.edit(None)
        elif selection == 2:
            self.list(None)
        elif selection == 3:
            self.enable(None)
        elif selection == 4:
            self.enableAll()
        elif selection == 5:
            self.disable(None)
        elif selection == 6:
            self.disableAll()
        elif selection == 7:
            self.delete(None)
        elif selection == 8:
            self.deleteAll()
        else:
            print("Unknown selection: %s" % selection)

    def new(self):
        items = [
            "Select minutes from now",
            "Select hours / minutes from now",
            "Select a time hours / minutes",
            "Enter a time (HH:MM)"
        ]
        self.show_quick_panel(items, self.handleNew)

    def edit(self, alarmId):
        if alarmId is -1:
            return
        if alarmId is None:
            items = self.getItems()
            if len(items):
                self.show_quick_panel(items, self.edit)
            else:
                sublime.status_message("No alarms to edit")
                return self.new()
        else:
            self.clearLocalVars()
            self.command = "edit"
            self.alarmId = alarmId
            items = [
                "Select minutes from now",
                "Select hours / minutes from now",
                "Select a time hours / minutes",
                "Enter a time (HH:MM)"
            ]
            self.show_quick_panel(items, self.handleEdit)

    def list(self, alarmId):
        if alarmId is -1:
            return
        if alarmId is None:
            items = self.getItems()
            if len(items):
                self.show_quick_panel(items, self.list)
            else:
                sublime.status_message("No alarms to list")
        else:
            self.clearLocalVars()
            self.command = "list"
            self.alarmId = alarmId
            alarms = self.getAlarmSettings()
            enabled = "Enable"
            try:
                self.listEnable = alarms[alarmId]["enabled"] is False
                enabled = "Disable" if alarms[alarmId]["enabled"] else "Enable"
            except:
                print("Can't find enabled.")

            displayTime = self.display(alarms[alarmId]["time"])
            items = [
                "Edit: %s" % displayTime,
                "%s: %s" % (enabled, displayTime),
                "Delete: %s" % displayTime
            ]
            self.show_quick_panel(items, self.handleList)

    def enable(self, alarmId):
        if alarmId is -1:
            return
        if alarmId is None:
            items = self.getItems()
            if len(items):
                self.show_quick_panel(items, self.enable)
            else:
                sublime.status_message("No alarms to enable")
        else:
            alarms = self.getAlarmSettings()
            try:
                alarms[alarmId]["enabled"] = True
                msg = "Enabling %s" % self.display(alarms[alarmId]["time"])
                print(msg)
                sublime.status_message(msg)
                self.saveAlarmSettings(alarms)
            except:
                print("Unable to find alarm to enable")

    def disable(self, alarmId):
        if alarmId is -1:
            return
        if alarmId is None:
            items = self.getItems()
            if len(items):
                self.show_quick_panel(items, self.disable)
            else:
                sublime.status_message("No alarms to disable")
        else:
            alarms = self.getAlarmSettings()
            try:
                alarms[alarmId]["enabled"] = False
                msg = "Disabling %s" % self.display(alarms[alarmId]["time"])
                print(msg)
                sublime.status_message(msg)
                self.saveAlarmSettings(alarms)
            except:
                print("Unable to find alarm to disable")

    def enableAll(self):
        alarms = self.getAlarmSettings()
        key = 0
        for alarm in alarms:
            alarms[key]["enabled"] = True
            key += 1
        self.saveAlarmSettings(alarms)
        msg = "Enabling all"
        print(msg)
        sublime.status_message(msg)

    def disableAll(self):
        alarms = self.getAlarmSettings()
        key = 0
        for alarm in alarms:
            alarms[key]["enabled"] = False
            key += 1
        self.saveAlarmSettings(alarms)
        msg = "Disabling all"
        print(msg)
        sublime.status_message(msg)

    def delete(self, alarmId):
        if alarmId is -1:
            return
        if alarmId is None:
            items = self.getItems()
            if len(items):
                self.show_quick_panel(items, self.delete)
            else:
                msg = "No alarms to delete"
                print(msg)
                sublime.status_message(msg)
        else:
            alarms = self.getAlarmSettings()
            try:
                msg = "Deleting %s" % self.display(alarms[alarmId]["time"])
                print(msg)
                sublime.status_message(msg)
                del alarms[alarmId]
                self.saveAlarmSettings(alarms)
            except:
                print("Unable to find alarm to delete")

    def deleteAll(self):
        if sublime.ok_cancel_dialog(
            "Are you sure you want to delete all alarms?",
            "Delete all"
        ):
            self.saveAlarmSettings([])
            msg = "All alarms deleted"
            print(msg)
            sublime.status_message(msg)

    def handleNew(self, selection):
        self.clearLocalVars()
        self.command = "new"

        if selection == 0:
            self.showMins()
        elif selection == 1:
            self.showHrs()
        elif selection == 2:
            self.showHrsDay()
        elif selection == 3:
            caption = "Enter time (HH:MM)"
            self.show_input_panel(
                caption,
                "",
                self.handleTime,
                self.handleChange,
                self.handleCancel
            )
        else:
            self.clearLocalVars()
            return

    def handleEdit(self, selection):
        if selection == 0:
            self.showMins()
        elif selection == 1:
            self.showHrs()
        elif selection == 2:
            self.showHrsDay()
        elif selection == 3:
            caption = "Enter time (HH:MM)"
            self.show_input_panel(
                caption,
                "",
                self.handleTime,
                self.handleChange,
                self.handleCancel
            )
        else:
            self.clearLocalVars()
            return

    def handleList(self, selection):
        if selection == 0:
            self.edit(self.alarmId)
        elif selection == 1:
            if self.listEnable:
                self.enable(self.alarmId)
            else:
                self.disable(self.alarmId)
        elif selection == 2:
            self.delete(self.alarmId)
        else:
            self.clearLocalVars()
            return

    def showMins(self):
        items = []
        if self.hrs:
            for min in range(1, 61):
                items.append(
                    [
                        "%d minute%s" % (
                            min,
                            "" if min is 1 else "s"
                        ),
                        "and %s hour%s from now" % (
                            self.hrs,
                            "" if self.hrs is 1 else "s"
                        )
                    ]
                )
        else:
            for min in range(1, 61):
                items.append(
                    "%d minute%s from now" % (min, "" if min is 1 else "s")
                )
        self.show_quick_panel(items, self.handleMins)

    def showMinsPast(self):
        items = []
        for min in range(0, 60):
            items.append("%02d past" % (min))
        self.show_quick_panel(items, self.handleMinsPast)

    def showHrs(self):
        items = []
        for hr in range(1, 25):
            items.append("%d hour%s from now" % (hr, "" if hr is 1 else "s"))
        self.show_quick_panel(items, self.handleHrs)

    def showHrsDay(self):
        items = []
        self.hrsNow = int(time.strftime("%H"))
        for h in range(0, 24):
            items.append("%02d:00" % ((h + self.hrsNow) % 24))
        self.show_quick_panel(items, self.handleHrsDay)

    def handleMins(self, selection):
        if selection is -1:
            return
        self.mins = selection + 1
        if self.hrs:
            msg = "New alarm in %s hour%s, %s min%s from now" % (
                self.hrs,
                "" if self.hrs is 1 else "s",
                self.mins,
                "" if self.mins is 1 else "s"
            )
            print(msg)
            sublime.status_message(msg)
            self.setAlarm(self.hrs, self.mins, False)
        else:
            msg = "New alarm in %s min%s from now" % (
                self.mins,
                "" if self.mins is 1 else "s"
            )
            print(msg)
            sublime.status_message(msg)
            self.setAlarm(0, self.mins, False)

    def handleMinsPast(self, selection):
        if selection is -1:
            return
        self.minsAt = selection
        msg = "New alarm at %02d:%02d" % (
            self.hrsAt % 24,
            self.minsAt
        )
        print(msg)
        sublime.status_message(msg)
        self.hrs = (self.hrsAt - int(time.strftime("%H"))) % 24
        self.mins = self.minsAt - int(time.strftime("%M"))
        if self.mins < 0:
            self.mins += 60
            self.hrs -= 1
        if self.hrs < 0:
            self.hrs += 24
        if not self.mins + self.hrs:
            self.mins = 1
        self.setAlarm(self.hrs, self.mins, True)

    def handleHrs(self, selection):
        if selection is -1:
            return
        self.hrs = selection + 1
        self.showMins()

    def handleHrsDay(self, selection):
        if selection is -1:
            return
        self.hrsAt = selection + self.hrsNow
        self.showMinsPast()

    def handleTime(self, timeOfDay):
        if ":" in timeOfDay:
            # If colon present then assume we have HH:MM
            self.hrsAt = int(timeOfDay[0:timeOfDay.find(":")])
            self.minsAt = int(timeOfDay[timeOfDay.find(":") + 1:])
        else:
            # If no colon then assume it's x mins past hour
            if int(timeOfDay) < int(time.strftime("%M")):
                self.hrsAt = int(time.strftime("%H")) + 1
            else:
                self.hrsAt = int(time.strftime("%H"))
            self.minsAt = int(timeOfDay)
        msg = "New alarm at %02d:%02d" % (
            self.hrsAt % 24,
            self.minsAt
        )
        print(msg)
        sublime.status_message(msg)
        self.hrs = self.hrsAt - int(time.strftime("%H"))
        self.mins = self.minsAt - int(time.strftime("%M"))
        if self.mins < 0:
            self.mins += 60
            self.hrs -= 1
        if self.hrs < 0:
            self.hrs += 24
        self.setAlarm(self.hrs, self.mins, True)

    def setAlarm(self, hrsD, minsD, at):
        msg = "Setting alarm for %s hour%s and %s minute%s in the future." % (
            hrsD,
            "" if hrsD is 1 else "s",
            minsD,
            "" if minsD is 1 else "s"
        )
        print(msg)
        sublime.status_message(msg)
        secsAway = (hrsD * 3600) + (minsD * 60)
        if at:
            secsAway -= int(time.strftime("%S"))
        sublime.set_timeout(
            self.ringMyBell,
            secsAway * 1000
        )
        # store the alarm
        alarms = self.getAlarmSettings()
        newTime = (
            datetime.datetime.now() + datetime.timedelta(0, secsAway)
        ).strftime(self.storageFormat)
        if self.command == "new":
            alarms.append(
                {"time": newTime, "enabled": True}
            )
        elif self.command == "edit":
            alarms[self.alarmId]["time"] = newTime
        self.saveAlarmSettings(alarms)

    def getSettings(self):
        if not self.settings:
            self.settings = sublime.load_settings(self.alarmSettingFile)
        return self.settings

    def chdirToPluginPath(self):
        pluginPath = os.path.dirname(os.path.abspath(__file__))
        # ST2 on XP managed to get the path wrong with the above line
        if not os.path.exists(os.path.join(pluginPath, "alarmclock.py")):
            pluginPath = os.path.join(
                sublime.packages_path(),
                "AlarmClock"
            )
        os.chdir(pluginPath)

    def getAlarmSettings(self):
        return self.getSettings().get("alarms", [])

    def saveAlarmSettings(self, alarms):
        self.getSettings().set("alarms", alarms)
        sublime.save_settings(self.alarmSettingFile)

    def getItems(self):
        alarms = self.getAlarmSettings()
        items = []
        if len(alarms):
            for alarm in alarms:
                items.append(
                    [
                        self.display(alarm["time"]),
                        "Enabled" if alarm["enabled"] else "Disabled"
                    ]
                )
        return items

    def ringMyBell(self):
        # Remove from alarm list
        alarms = self.getAlarmSettings()
        found = False
        key = 0
        toDel = []
        currentTime = time.time()
        for alarm in alarms:
            alarmTime = time.mktime(
                time.strptime(alarm["time"], self.storageFormat)
            )
            if abs(alarmTime - currentTime) < 55:
                if alarm["enabled"]:
                    found = True
                toDel.append(key)
            key += 1
        if len(toDel):
            for d in reversed(toDel):
                del alarms[d]
        self.saveAlarmSettings(alarms)
        if found:
            self.startBeeping()
            if sublime.ok_cancel_dialog("Alarm time up", "Snooze"):
                sublime.set_timeout(
                    self.snoozeMyBell,
                    (self.getSettings().get(
                        "snooze_mins",
                        self.snoozeTimeMins
                    ) * 60) * 1000
                )
            self.stopBeeping()
        else:
            print("Ring my bell hit but no alarm set")

    def snoozeMyBell(self):
        self.startBeeping()
        if sublime.ok_cancel_dialog("Snooze time up", "Snooze again"):
            sublime.set_timeout(
                self.snoozeMyBell,
                (self.getSettings().get(
                    "snooze_mins",
                    self.snoozeTimeMins
                ) * 60) * 1000
            )
        self.stopBeeping()

    def onAppStart(self):
        alarms = self.getAlarmSettings()
        alarms = self.removeOldAlarms(alarms)
        key = 0
        currentTime = time.time()
        for alarm in alarms:
            alarmTime = time.mktime(
                time.strptime(alarm["time"], self.storageFormat)
            )
            sublime.set_timeout(
                self.ringMyBell,
                (alarmTime - currentTime) * 1000
            )
            key += 1
        self.saveAlarmSettings(alarms)
        self.chdirToPluginPath()
        platform = sublime.platform()
        if platform == "linux":
            os.chmod("alarms/linux_alarm.sh", 0o777)
        elif platform == "osx":
            os.chmod("alarms/osx_alarm.sh", 0o777)

    def removeOldAlarms(self, alarms):
        key = 0
        toDel = []
        currentTime = time.time()
        for alarm in alarms:
            alarmTime = time.mktime(
                time.strptime(alarm["time"], self.storageFormat)
            )
            if alarmTime < currentTime:
                toDel.append(key)
            key += 1
        if len(toDel):
            for d in reversed(toDel):
                del alarms[d]
        return alarms

    def startBeeping(self):
        self.beeper = False
        if self.getSettings().get("audible", True):
            self.chdirToPluginPath()
            platform = sublime.platform()
            if platform == "windows":
                # Windows XP, vista, 7
                beepCmd = self.getSettings().get("win_alarm_cmd", None)
            elif platform == "linux":
                # Alsa required
                beepCmd = self.getSettings().get("linux_alarm_cmd", None)
            elif platform == "osx":
                if self.getSettings().get("osx_say", None):
                    beepCmd = ["say", self.getSettings().get("osx_say", None)]
                else:
                    # OSX 10.5+?
                    beepCmd = self.getSettings().get("osx_alarm_cmd", None)
            else:
                print("Platform not supported")
                return
            self.beeper = subprocess.Popen(beepCmd)

    def stopBeeping(self):
        if self.beeper:
            try:
                self.beeper.terminate()
            except:
                pass

    def display(self, t):
        return time.strftime(
            self.displayFormat,
            time.strptime(t, self.storageFormat)
        )

    def show_quick_panel(self, options, done):
        sublime.set_timeout(
            lambda: self.view.window().show_quick_panel(options, done),
            10
        )

    def show_input_panel(self, caption, initialtext, done, change, cancel):
        sublime.set_timeout(
            lambda: self.view.window().show_input_panel(
                caption,
                initialtext,
                done,
                change,
                cancel
            ),
            10
        )

    def clearLocalVars(self):
        self.command = None
        self.mins = None
        self.hrs = None
        self.minsAt = None
        self.hrsAt = None
        self.hrsNow = None

    def handleChange(self, selection):
        return

    def handleCancel(self):
        return


def plugin_loaded():
    sublime.active_window().run_command(
        "alarm_clock",
        {"action": "on_app_start"}
    )

if int(sublime.version()) < 3000:
    sublime.set_timeout(lambda: plugin_loaded(), 2000)
