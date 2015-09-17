import sublime
import sublime_plugin
import urllib.request
import urllib.parse
import json


class codicReplaceWordCommand(sublime_plugin.TextCommand):
    def run(self, edit, casing="camel", project_id=None, selection_word=None):
        sels = self.view.sel()
        for sel in sels:
            selection_word = self.view.substr(sel)
        if selection_word == '':
            # self.window = sublime.active_window()
            # self.window.run_command("codic_replace_word")
            sublime.status_message('No word was selected.')
            return

        url = getApiUrl()+'/engine/translate.json'
        values = {
            'text': selection_word,
            'casing': casing
        }

        if project_id is not None:
            values['project_id'] = project_id

        headers = getAutorizationHeader()

        req = requestApi(url, values, headers)

        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            data = json.loads(the_page.decode('utf-8'))
            if data[0]['successful']:
                result = data[0]['translated_text']
                self.view.replace(edit, sel, result)


class codicGetProjectIdsCommand(sublime_plugin.TextCommand):
    """docstring for getProjectId"""
    def run(self, edit):
        self.items = []

        url = getApiUrl()+'/user_projects.json'
        values = {
        }
        headers = getAutorizationHeader()
        req = requestApi(url, values, headers)

        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            data = json.loads(the_page.decode('utf-8'))
            for res_data in data:
                proj_id = str(res_data['id'])
                name = res_data['name']
                desc = res_data['description']
                self.items.append([proj_id, name, desc])
            self.window = sublime.active_window()
            self.window.show_quick_panel(self.items, self.on_done)

    def on_done(self, index):
        proj_id = self.items[index][0]
        self.window.run_command("codic_replace_word", {
            "casing": "camel", "project_id": proj_id
        })


class codicInputWordCommand(sublime_plugin.TextCommand):
    """docstring for inputTranslationWord"""
    def run(self, edit):
        self.window = sublime.active_window()
        self.window.show_input_panel("codic input word", "", self.on_done, self.on_change, self.on_cancel)

    def on_done(self, word):
        print(word)
        self.window.run_command("codic_replace_word", {
            "word": word
        })

    def on_cancel(self):
        pass

    def on_change():
        pass


def requestApi(url, values, headers):
    data = urllib.parse.urlencode(values)
    full_url = url+'?'+data
    req = urllib.request.Request(full_url, None, headers, None, False, 'GET')
    return req


def getSettings():
    return sublime.load_settings("codic.sublime-settings")


def getApiUrl():
    return getSettings().get('api_url')


def getAutorizationHeader():
    access_token = getSettings().get('access_token')
    return {'Authorization': 'Bearer '+access_token}
