# import time
# from time import sleep
# import string
# import random
# import math


# class RingMenu:
# 	def __init__(self, display_subject, menu_items, index=0):
#         self.display_subject = display_subject
#         self.menu_items = menu_items
#         self.index = index

#     def update_display(self):

#         # updating display
#         delta_time = time.time() - self.last_time
#         self.last_time = time.time()

#     def add_index(self, amt):
#         self.index += amt
#         self._update_menu()

#     def _update_menu(self):
#         selection = self.menu_items[self.index%len(self.menu_items)]
#         display_subject.send(selection)