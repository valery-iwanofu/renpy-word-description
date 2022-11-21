init python:
    GlossaryWord(
        uid='long_word',
        word=_('Word with long description'),
        description=_('Very long description in width, so long that it should be in the middle of the screen (elongation techniqueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee)')
    )
    GlossaryWord(
        uid='tall_word',
        word=_('Word with "tall" description'),
        description='\n'.join(f'Line {i}' for i in range(10))
    )
    GlossaryWord(
        uid='normal_word',
        word=_('Normal word'),
        description=_('Short description'),
        note=_('Note')
    )

    GlossaryWord(
        uid='unique_word_id',
        word=_('Tatakae'),
        description=_('Means fight in Japanese.')
    )

label start:
    scene expression '#1100ffff'
    'Hello... {glossary=tall_word}word{/glossary}. OOOOOOOOOOOOOOO. {glossary=long_word}Capitalized word{/glossary}. {glossary=normal_word}Short word{/glossary}.'

    'Eren' '{glossary=unique_word_id}Tatakae, tatakae, tatakae{/glossary}.'
    'Hange' 'Are you mad?'

    return
