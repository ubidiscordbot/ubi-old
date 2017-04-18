import shutil
import json


def install(source_path, settings_path):
    f = open(settings_path, "r")
    f_ = json.loads(f.read())
    name_ = f_["Name"]
    shutil.copyfile(source_path, "lib/modules/ext/" + name_ + ".py")
    shutil.copyfile(settings_path, "lib/modules/ext/commands/" + name_ + ".json")


def server_install(module_name, serverid):
    f = open("server/servers/" + serverid + ".json", "r")
    f_ = json.loads(f.read())
    f.close()
    f = open("server/servers/" + serverid + ".json", "w")
    fm = open("lib/modules/ext/commands/" + module_name + ".json", "r")
    fm_ = json.loads(fm.read())
    fm.close()
    f_[fm_["Name"]] = fm_["Commands"]
    f.write(json.dumps(f_))
    f.close()

server_install("coolModule", "297598358372220928")