from tkinter import ttk
import tkinter as tk

import inspect

CLASS_INSPECTOR_WAS_ACTIVATED = False


class InteractiveClassInspector:
    def __init__(self, root, obj, name="ROOT", max_depth=20, show_private=False, show_inherited=True):
        global CLASS_INSPECTOR_WAS_ACTIVATED

        CLASS_INSPECTOR_WAS_ACTIVATED = True

        self.root = root
        self.max_depth = max_depth
        self.show_private = show_private
        self.show_inherited = show_inherited
        self.visited = set()
        self.object_data = {}

        self.root.title(f"Class inspector - {name}")
        self.root.geometry("1000x700")

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        self.show_private_var = tk.BooleanVar(value=show_private)
        private_cb = ttk.Checkbutton(
            control_frame,
            text="Show private attributes",
            variable=self.show_private_var,
            command=self.refresh_tree
        )
        private_cb.pack(side=tk.LEFT)

        self.show_inherited_var = tk.BooleanVar(value=show_inherited)
        inherited_cb = ttk.Checkbutton(
            control_frame,
            text="Show inherited attributes",
            variable=self.show_inherited_var,
            command=self.refresh_tree
        )
        inherited_cb.pack(side=tk.LEFT, padx=(10, 0))

        refresh_btn = ttk.Button(
            control_frame,
            text="Update",
            command=self.refresh_tree
        )
        refresh_btn.pack(side=tk.LEFT, padx=(10, 0))

        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("type", "value"), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("value", text="Value")

        self.tree.column("#0", width=300)
        self.tree.column("type", width=150)
        self.tree.column("value", width=400)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        info_frame = ttk.LabelFrame(main_frame, text="Information")
        info_frame.pack(fill=tk.X, pady=(10, 0))

        self.info_text = tk.Text(info_frame, height=9, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)

        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.root_object = obj
        self.root_name = name

        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        self.tree.bind("<Button-1>", self.on_tree_click)

        self.icons = {
            'class': '📁',
            'object': '🔷',
            'dict': '📘',
            'list': '📋',
            'tuple': '📋',
            'method': '⚡',
            'function': '🔧',
            'variable': '📄',
            'property': '🏷️',
            'error': '❌',
            'circular': '🔄',
            'inherited': '🔗'
        }

        self.populate_tree()

    def refresh_tree(self):
        self.show_private = self.show_private_var.get()
        self.show_inherited = self.show_inherited_var.get()
        self.visited.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.object_data.clear()

        self.populate_tree()

    def populate_tree(self):
        root_icon = self.get_icon(self.root_object)
        root_type = type(self.root_object).__name__

        root_item = self.tree.insert(
            "", "end",
            text=f"{root_icon} {self.root_name}",
            values=(root_type, self.safe_repr(self.root_object)),
            open=True
        )

        self.object_data = {}
        self.object_data[root_item] = {
            "object": self.root_object,
            "depth": 0,
            "obj_id": id(self.root_object),
            "attr_name": self.root_name,
            "is_inherited": False
        }

        self.add_children(root_item, self.root_object, 1)

    def is_attribute_inherited(self, obj, attr_name):
        try:
            if not inspect.isclass(obj):
                obj_class = type(obj)

            else:
                obj_class = obj

            if hasattr(obj, '__dict__') and attr_name in obj.__dict__:
                return False

            if inspect.isclass(obj_class):
                for i, cls in enumerate(obj_class.__mro__):
                    if attr_name in cls.__dict__:
                        return i > 0

            return False

        except Exception:
            return False

    def add_children(self, parent_item, obj, depth):
        if depth > self.max_depth:
            self.tree.insert(parent_item, "end", text="⚠️ Max depth")
            return

        obj_id = id(obj)
        if obj_id in self.visited:
            self.tree.insert(parent_item, "end", text="🔄 Circular link")
            return

        self.visited.add(obj_id)

        try:
            attributes = self.get_all_attributes(obj)
            filtered_attrs = self.filter_attributes(attributes, obj)

            sorted_attrs = sorted(filtered_attrs.items(), key=lambda x: (
                not inspect.isclass(x[1]),
                not isinstance(x[1], (dict, list, tuple, set, frozenset)),
                not callable(x[1]),
                x[0].lower()
            ))

            for name, value in sorted_attrs:
                is_inherited = self.is_attribute_inherited(obj, name)
                self.add_attribute_node(parent_item, name, value, depth, is_inherited)

        except Exception as e:
            self.tree.insert(
                parent_item, "end",
                text=f"❌ Error: {str(e)}",
                values=("error", "")
            )
        finally:
            self.visited.discard(obj_id)

    def add_attribute_node(self, parent_item, name, value, depth, is_inherited=False):
        icon = self.get_icon(value)

        if is_inherited and not isinstance(value, (dict, list, tuple, set, frozenset)):
            icon = self.icons['inherited']

        value_type = type(value).__name__
        value_repr = self.safe_repr(value)

        if isinstance(value, dict):
            display_name = f"{icon} {name} [{len(value)} elements]"
        elif isinstance(value, (list, tuple, set, frozenset)):
            display_name = f"{icon} {name} [{len(value)} elements]"
        elif inspect.isclass(value):
            display_name = f"{icon} {name} (class {value.__name__})"
        elif callable(value):
            sig = self.get_function_signature(value)
            display_name = f"{icon} {name}{sig}"
        else:
            display_name = f"{icon} {name}"

        item = self.tree.insert(
            parent_item, "end",
            text=display_name,
            values=(value_type, value_repr)
        )

        self.object_data[item] = {
            "object": value,
            "depth": depth,
            "obj_id": id(value),
            "attr_name": name,
            "is_inherited": is_inherited
        }

        if self.should_have_children(value):
            self.tree.insert(item, "end", text="Loading...")

    def should_have_children(self, obj):
        if inspect.isclass(obj):
            return True
        if isinstance(obj, (dict, list, tuple, set, frozenset)) and obj:
            return True
        if hasattr(obj, '__dict__') and not isinstance(obj, (str, int, float, bool, bytes)):
            return True
        if hasattr(obj, '__slots__'):
            return True
        return False

    def get_all_attributes(self, obj):
        attributes = {}

        if isinstance(obj, dict):
            for key, value in obj.items():
                attributes[f"[{self.safe_repr(key, 20)}]"] = value
            return attributes

        if isinstance(obj, (list, tuple, set, frozenset)):
            for i, value in enumerate(obj):
                attributes[f"[{i}]"] = value
            return attributes

        for attr_name in dir(obj):
            try:
                attributes[attr_name] = getattr(obj, attr_name)
            except Exception as e:
                attributes[attr_name] = e  # сохраняем объект ошибки

        if hasattr(obj, '__dict__'):
            attributes.update(obj.__dict__)

        if inspect.isclass(obj):
            for cls in obj.__mro__:
                if hasattr(cls, '__dict__'):
                    for name, value in cls.__dict__.items():
                        if name not in attributes:
                            attributes[name] = value

        return attributes

    def filter_attributes(self, attributes, obj):
        filtered = {}

        for name, value in attributes.items():
            system_attrs = {
                '__dict__', '__weakref__', '__module__', '__qualname__',
                '__annotations__', '__orig_bases__', '__parameters__',
                '__doc__', '__name__', '__package__', '__spec__',
                '__cached__', '__file__', '__loader__'
            }

            if name in system_attrs:
                continue

            if name.startswith('_') and not self.show_private:
                continue

            if not self.show_inherited and self.is_attribute_inherited(obj, name):
                continue

            filtered[name] = value

        return filtered

    def get_icon(self, obj):
        if inspect.isclass(obj):
            return self.icons['class']
        elif isinstance(obj, dict):
            return self.icons['dict']
        elif isinstance(obj, (list, tuple, set, frozenset)):
            return self.icons['list']
        elif inspect.ismethod(obj):
            return self.icons['method']
        elif inspect.isfunction(obj):
            return self.icons['function']
        elif hasattr(obj, '__dict__') and not isinstance(obj, (str, int, float, bool, bytes)):
            return self.icons['object']
        else:
            return self.icons['variable']

    def get_function_signature(self, func):
        try:
            sig = inspect.signature(func)
            return str(sig)
        except:
            return "()"

    def safe_repr(self, obj, max_len=9999):
        try:
            if isinstance(obj, Exception):
                repr_str = f"<Access error: {obj}>"
            elif isinstance(obj, str):
                repr_str = f'"{obj}"'
            else:
                repr_str = repr(obj)

            if len(repr_str) > max_len:
                return repr_str[:max_len] + "..."
            return repr_str
        except Exception as e:
            return f"<repr error: {e}>"

    def on_tree_click(self, event):
        try:
            item = self.tree.identify_row(event.y)
            if not item:
                return

            region = self.tree.identify_region(event.x, event.y)
            if region == "tree":
                children = self.tree.get_children(item)
                if (children and len(children) == 1 and
                    self.tree.item(children[0])['text'] == 'Loading...'):

                    self.tree.delete(children[0])

                    if item in self.object_data:
                        obj = self.object_data[item]["object"]
                        depth = self.object_data[item]["depth"]
                        self.add_children(item, obj, depth + 1)
        except Exception as e:
            print(f"Click error: {e}")

    def on_item_select(self, event):
        self.info_text.delete(1.0, tk.END)

        try:
            selection = self.tree.selection()
            if not selection:
                self.info_text.insert(tk.END, "No element selected")
                return

            item = selection[0]

            if item not in self.object_data:
                self.info_text.insert(tk.END, "Object data not available")
                return

            data = self.object_data[item]
            obj = data["object"]
            attr_name = data["attr_name"]
            depth = data["depth"]
            is_inherited = data.get("is_inherited", False)

            info_lines = []
            info_lines.append(f"Name: {attr_name}")
            info_lines.append(f"Type: {type(obj).__name__}")
            info_lines.append(f"ID: {id(obj)}")
            info_lines.append(f"Depth: {depth}")

            if is_inherited:
                info_lines.append("Status: Inherited attribute 🔗")
                try:
                    parent_obj = None
                    parent_item = self.tree.parent(item)
                    if parent_item and parent_item in self.object_data:
                        parent_obj = self.object_data[parent_item]["object"]

                    if parent_obj and inspect.isclass(type(parent_obj)):
                        for i, cls in enumerate(type(parent_obj).__mro__):
                            if hasattr(cls, '__dict__') and attr_name in cls.__dict__:
                                if i > 0:
                                    info_lines.append(f"Defined in class: {cls.__name__}")
                                break
                except:
                    pass
            else:
                info_lines.append("Status: Own attribute")

            if hasattr(obj, '__module__'):
                module = getattr(obj, '__module__')
                if module and module != 'builtins':
                    info_lines.append(f"Module: {module}")

            if hasattr(obj, '__len__'):
                try:
                    length = len(obj)
                    info_lines.append(f"Length: {length}")
                except:
                    pass

            if inspect.isclass(obj):
                info_lines.append(f"This is class: {obj.__name__}")

                if obj.__bases__:
                    bases = [base.__name__ for base in obj.__bases__]
                    info_lines.append(f"Inherits from: {', '.join(bases)}")

                mro_classes = [cls.__name__ for cls in obj.__mro__[:5]]
                if len(obj.__mro__) > 5:
                    mro_classes.append("...")
                info_lines.append(f"MRO: {' -> '.join(mro_classes)}")

            elif callable(obj):
                func_name = getattr(obj, '__name__', 'unnamed')
                info_lines.append(f"Function: {func_name}")

                try:
                    sig = inspect.signature(obj)
                    info_lines.append(f"Signature: {func_name}{sig}")
                except:
                    info_lines.append("Signature not available")

            elif isinstance(obj, (str, int, float, bool, type(None))):
                value_repr = self.safe_repr(obj, 100)
                info_lines.append(f"Value: {value_repr}")

            if hasattr(obj, '__dict__'):
                try:
                    attrs = [k for k in obj.__dict__.keys() if not k.startswith('__')]
                    if attrs:
                        info_lines.append(f"Attributes: {len(attrs)}")
                except:
                    pass

            tree_values = self.tree.item(item)['values']
            if tree_values and len(tree_values) >= 2:
                tree_value = tree_values[1]
                if tree_value and tree_value.strip():
                    info_lines.append(f"Display value: {tree_value}")

            result_text = "\n".join(info_lines)
            self.info_text.insert(tk.END, result_text)

        except Exception as e:
            error_msg = f"Error getting information: {str(e)}\n"
            error_msg += f"Error type: {type(e).__name__}\n"
            self.info_text.insert(tk.END, error_msg)

    def on_search(self, *args):
        search_text = self.search_var.get().lower()
        if not search_text:
            return
        self.search_in_tree("", search_text)

    def search_in_tree(self, item, search_text):
        children = self.tree.get_children(item)
        for child in children:
            text = self.tree.item(child)['text'].lower()
            if search_text in text:
                parent = self.tree.parent(child)
                while parent:
                    self.tree.item(parent, open=True)
                    parent = self.tree.parent(parent)

                self.tree.selection_set(child)
                self.tree.focus(child)
                self.tree.see(child)
                return True
            if self.search_in_tree(child, search_text):
                return True
        return False


def inspector(obj, name="ROOT", max_depth=20, show_private=False, show_inherited=False) -> None:
    if CLASS_INSPECTOR_WAS_ACTIVATED:
        return

    root = tk.Tk()
    app = InteractiveClassInspector(root, obj, name, max_depth, show_private, show_inherited)
    root.mainloop()
