import sublime
import sublime_plugin
import urllib.request
import urllib.parse
import json


class codicTranslateStringCommand(sublime_plugin.TextCommand):
    def run(self, edit, casing=None, project_id=None, input_word=None):
        input_flag = False
        if input_word is None:
            sels = self.view.sel()
            for sel in sels:
                selection_word = self.view.substr(sel)
            if selection_word is None or selection_word == '':
                sublime.active_window().run_command('codic_input_string')
        else:
            selection_word = input_word
            input_flag = True

        if selection_word == '':
            sublime.status_message('No word was selected.')
            return

        casing = setCasingSetting(casing)
        acronym_style = getAcronymStyleSetting()

        url = getApiUrl()+'/engine/translate.json'
        values = {
            'text': selection_word,
            'casing': casing,
            'acronym_style': acronym_style
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
                if input_flag:
                    self.view.insert(edit, self.view.sel()[0].a, result)
                else:
                    self.view.replace(edit, sel, result)


class codicGetProjectIdsCommand(sublime_plugin.TextCommand):
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


class codicInputStringCommand(sublime_plugin.TextCommand):
    """docstring for inputTranslationWord"""
    def run(self, edit):
        self.window = sublime.active_window()
        self.window.show_input_panel("codic input string", "", self.on_done, self.on_change, self.on_cancel)

    def on_done(self, word):
        self.window.run_command("codic_translate_string", {
            "input_word": word
        })

    def on_cancel(self):
        pass

    def on_change(self):
        pass


def requestApi(url, values, headers):
    data = urllib.parse.urlencode(values)
    full_url = url+'?'+data
    print(full_url)
    req = urllib.request.Request(full_url, None, headers, None, False, 'GET')
    return req


def getSettings():
    return sublime.load_settings("codic.sublime-settings")


def getApiUrl():
    return getSettings().get('api_url')


def getAutorizationHeader():
    access_token = getSettings().get('access_token')
    return {'Authorization': 'Bearer '+access_token}


def setCasingSetting(casing):
    if casing is None:
        return getSettings().get('casing')
    return casing


def getAcronymStyleSetting():
    return getSettings().get('acronym_style')
