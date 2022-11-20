screen glossary_word(word_uid):
    $ word = get_glossary_word_by_uid(word_uid)
    $ focus_rect = GetFocusRect('glossary_tooltip')
    if focus_rect:
        fixed:
            xfit True
            yfit True
            use glossary_word_frame(word, focus_rect)

screen glossary_word_frame(word, focus_rect):
    frame:
        # it is better to make the maximum width smaller
        # 1350 using for test __FitChild
        xmaximum 1800
        #xmaximum 400

        # __FitChild will place frame at the screen so that it doesn't go off the screen
        at renpy.curry(__FitChild)(focus_rect=focus_rect)

        style_prefix 'glossary'

        has vbox
        text word.word style_suffix 'title_text'
        text word.description style_suffix 'description_text'


style glossary_button is default
style glossary_button_text is default

style glossary_title_text is text:
    size 30

style glossary_description_text is text:
    size 20

init -1 python:
    GLOSSARY_WORDS = {}

    def get_glossary_word_by_uid(uid):
        return GLOSSARY_WORDS[uid]

    class GlossaryWord:
        def __init__(self, uid, word, description):
            self.uid = uid
            self.word = word
            self.description = description
            GLOSSARY_WORDS[uid] = self
        
        def __reduce__(self):
            return get_glossary_word_by_uid, (self.uid, )

init python:
    def glossary_tag(tag, argument, contents):
        # https://github.com/renpy/renpy/issues/4102
        if len(contents) == 0:
            # TODO maybe, this is bad idea
            text = GLOSSARY_WORDS[argument].word
        elif len(contents) == 1 and contents[0][0] == renpy.TEXT_TEXT:
            text = contents[0][1]
        else:
            raise ValueError('glossary tag should contain only text')

        return [
            (
                renpy.TEXT_DISPLAYABLE, 
                TextButton(
                    text, 
                    hovered=[CaptureFocus('glossary_tooltip'), Show('glossary_word', None, argument)],
                    unhovered=[ClearFocus('glossary_tooltip'), Hide('glossary_word')],
                    action=NullAction(),
                    style='glossary_button'
                )
            )
        ]

    config.custom_text_tags["glossary"] = glossary_tag

init python:
    class __FitChild(renpy.Displayable):
        def __init__(self, child, focus_rect, **kwargs):
            super(__FitChild, self).__init__(**kwargs)
            self.child = child
            self.focus_rect = focus_rect

        def visit(self):
            return [self.child]

        def render(self, width, height, st, at):
            child_render = renpy.render(self.child, width, height, st, at)

            cw, ch = child_render.width, child_render.height

            fx, fy, fw, fh = self.focus_rect

            possible_x = [
                fx + fw / 2 - cw / 2,  # in middle of focus_rect
                fx - cw,               # left of focus_rect
                fx                     # right of focus_rect
            ]
            possible_y = [
                fy + fh,  # under focus_rect
                fy - ch   # above focus_rect
            ]

            for x in possible_x:
                if x >= 0 and (x + cw) < width:
                    break
            else:
                # doesn't fit the screen by width
                x = width / 2 - cw / 2  # in middle of the screen by x axis

            for y in possible_y:
                if y >= 0 and (y + ch) < height:
                    break
            else:
                # doesn't fit the screen by height
                y = height / 2 - ch / 2  # in middle of the screen by y axis

            rv = renpy.Render(width, height)
            rv.blit(child_render, (x, y))

            return rv
