with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    content = f.read()

checks = ['<template>', '</template>', '<script setup', '</script>', '<style scoped>', '</style>',
          'choiceQuestions', 'loadAnswer', 'single-layout', 'sl-nav', 'sl-sheet',
          'renderText', 'renderedContent', 'COMPREHENSIVE', 'parsedListOptions',
          'initState', 'selectListOption', 'submitListAnswer', 'toggleFavorite']

for c in checks:
    if c in content:
        print(f'  [OK] {c}')
    else:
        print(f'  [MISSING] {c}')

# Check brace balance
open_braces = content.count('{{')
close_braces = content.count('}}')
print(f'\nTemplate braces: {{ = {open_braces}, }} = {close_braces}')
if open_braces != close_braces:
    print('WARNING: Mismatched!')
