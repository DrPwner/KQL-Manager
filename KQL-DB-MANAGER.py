import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
import json
import pyperclip


class QueryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Query Manager")
        self.root.geometry("1700x800")
        
        # Initialize database
        self.init_db()
        
        # Create menu
        self.create_menu()
        
        # Create navigation pane
        self.create_navigation_pane()
        
        # Create display area
        self.create_display_area()
        
        # Load queries
        self.load_queries()
        
    def init_db(self):
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            date_added TEXT NOT NULL,
            description TEXT,
            query_text TEXT NOT NULL,
            is_favorite BOOLEAN NOT NULL CHECK (is_favorite IN (0, 1)),
            tags TEXT
        )
        ''')
        conn.commit()
        conn.close()
        
    def create_menu(self):
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)

            file_menu = tk.Menu(menubar, tearoff=0)
            # Removed Add command
            file_menu.add_command(label="Export", command=self.export_data)
            file_menu.add_command(label="Import", command=self.import_data)
            file_menu.add_command(label="Exit", command=self.root.quit)
            menubar.add_cascade(label="File", menu=file_menu)

            edit_menu = tk.Menu(menubar, tearoff=0)
            edit_menu.add_command(label="Add", command=self.add_query)
            edit_menu.add_command(label="Edit", command=self.edit_query)
            edit_menu.add_command(label="Delete", command=self.delete_query)
            menubar.add_cascade(label="Edit", menu=edit_menu)

            search_menu = tk.Menu(menubar, tearoff=0)
            search_menu.add_command(label="Search", command=self.search_query)
            menubar.add_cascade(label="Search", menu=search_menu)
        
        #####WORKINGGGGGGGGGG DISPLAYINGGGGG TITLES NOT SHARMUTA ID'ssssss
        
    # def create_navigation_pane(self):
    #     nav_frame = ttk.Frame(self.root, width=4000)
    #     nav_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
    #     tk.Label(nav_frame, text="Navigation", font=('Arial', 16)).pack(expand=True, padx=50,)
        
    #     self.nav_tree = ttk.Treeview(nav_frame, padding=70)
    #     self.nav_tree.bind("<<TreeviewSelect>>", self.display_query_details)
    #     self.nav_tree.pack(fill=tk.BOTH, expand=True, ipadx=60)

    def display_query_details(self, event):
        selected_item = self.nav_tree.selection()
        if selected_item:
            query_id = self.nav_tree.item(selected_item[0], 'values')[0]
            conn = sqlite3.connect('queries.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM queries WHERE id = ?', (query_id,))
            query = cursor.fetchone()
            conn.close()
            
            if query:
                self.title_label.config(text=query[1])
                self.author_label.config(text=query[2])
                self.date_added_label.config(text=query[3])
                self.description_label.config(text=query[4])
                
                # Temporarily enable the text widget to update its content
                self.query_text_display.config(state=tk.NORMAL)
                self.query_text_display.delete(1.0, tk.END)
                self.query_text_display.insert(tk.END, query[5])
                self.query_text_display.config(state=tk.DISABLED)
                
                self.tags_label.config(text=query[7])




    def create_navigation_pane(self):
        # Create a frame for the navigation pane
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a label for the navigation section
        tk.Label(nav_frame, text="Navigation", font=('Arial', 16)).pack(padx=50)

        # Add a Treeview widget for displaying query titles
        self.nav_tree = ttk.Treeview(nav_frame)
        #self.nav_tree.heading('ID', text='ID')
       # self.nav_tree.heading('Title', text='KQL Query Titles', anchor='center')
        #self.nav_tree.column('ID', width=50, anchor='w')
        #self.nav_tree.column('Title', width=400, anchor='w')
        self.nav_tree.pack(fill=tk.BOTH, expand=True)

        # Bind the selection event to the display_query_details method
        self.nav_tree.bind("<<TreeviewSelect>>", self.display_query_details)


   # def create_navigation_pane(self):
    #     #done
    #     nav_frame = ttk.Frame(self.root)
    #     nav_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    #     #done
    #     tk.Label(nav_frame, text="Navigation", font=('Arial', 16)).pack(expand=True, padx=50,)
        
    #     self.nav_tree = ttk.Treeview(nav_frame, padding=70)
    #     self.nav_tree.bind("<<TreeviewSelect>>", self.display_query_details)
    #     self.nav_tree.pack(fill=tk.BOTH, expand=True, ipadx=60)




    # def create_navigation_pane(self):
    #     # Create a frame for the navigation pane
    #     nav_frame = ttk.Frame(self.root)
    #     nav_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    #     # Add a label for the navigation section
    #     tk.Label(nav_frame, text="Navigation", font=('Arial', 16)).pack(expand=True, padx=50,)
        
    #     # Add a Treeview widget for displaying query titles
    #     self.nav_tree = ttk.Treeview(nav_frame, padding=70)
    #     self.nav_tree = ttk.Treeview(nav_frame, columns=('Title'),show='headings')
    #     self.nav_tree.heading('Title', text='KQL Query Titles')
    #     self.nav_tree.pack(fill=tk.BOTH, expand=True)
    
    #     # Configure the Treeview column to auto-adjust width
    #     self.nav_tree.bind("<<TreeviewSelect>>", self.display_query_details)
        #self.nav_tree.column('Title', anchor='w', minwidth=100, width=400, stretch=True)
        
        # Bind the selection event to the display_query_details method
        



    

    # def create_navigation_pane(self):
    #     #done
    #     nav_frame = ttk.Frame(self.root)
    #     nav_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    #     #done
    #     tk.Label(nav_frame, text="Navigation", font=('Arial', 16)).pack(expand=True, padx=50,)
        
    #     self.nav_tree = ttk.Treeview(nav_frame, padding=70)
    #     self.nav_tree.bind("<<TreeviewSelect>>", self.display_query_details)
    #     self.nav_tree.pack(fill=tk.BOTH, expand=True, ipadx=60)






    # def create_navigation_pane(self):
    #     # Create a frame for the navigation pane
    #     nav_frame = ttk.Frame(self.root)
    #     nav_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    #     # Add a label for the navigation section
    #     tk.Label(nav_frame, text="Navigation", font=('Arial', 16)).pack(expand=True, padx=50)

    #     # Add a Treeview widget for displaying query titles
    #     self.nav_tree = ttk.Treeview(nav_frame, columns=('Title'), show='headings')
    #     self.nav_tree.heading('Title', text='KQL Query Titles')
    #     self.nav_tree.column('Title', anchor='w', minwidth=100, width=400, stretch=True)
    #     self.nav_tree.pack(fill=tk.BOTH, expand=True)

    #     # Add a vertical scrollbar to the Treeview
    #     self.tree_scrollbar = ttk.Scrollbar(nav_frame, orient=tk.VERTICAL, command=self.nav_tree.yview)
    #     self.nav_tree.configure(yscroll=self.tree_scrollbar.set)
    #     self.tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #     # Bind the selection event to the display_query_details method
    #     self.nav_tree.bind("<<TreeviewSelect>>", self.display_query_details)






    def create_display_area(self):
        self.display_frame = ttk.Frame(self.root)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(self.display_frame, text="Query Details", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.display_frame, text="Title:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.title_label = tk.Label(self.display_frame, text="", font=('Arial', 12))
        self.title_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.display_frame, text="Author:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.author_label = tk.Label(self.display_frame, text="", font=('Arial', 12))
        self.author_label.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.display_frame, text="Date Added:", font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.date_added_label = tk.Label(self.display_frame, text="", font=('Arial', 12))
        self.date_added_label.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.display_frame, text="Description:", font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.description_label = tk.Label(self.display_frame, text="", font=('Arial', 12))
        self.description_label.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.display_frame, text="Query Text:", font=('Arial', 12, 'bold')).grid(row=5, column=0, sticky='w', padx=10, pady=5)

        # Add the Copy button
        self.copy_button = tk.Button(self.display_frame, text="Copy Query", command=self.copy_to_clipboard)
        self.copy_button.grid(row=5, column=1, padx=(10, 0), pady=5, sticky='w')

        self.query_text_display = tk.Text(self.display_frame, wrap=tk.WORD, height=10, width=60, state=tk.DISABLED)
        self.query_text_display.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        tk.Label(self.display_frame, text="Tags:", font=('Arial', 12, 'bold')).grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.tags_label = tk.Label(self.display_frame, text="", font=('Arial', 12))
        self.tags_label.grid(row=7, column=1, padx=10, pady=5, sticky='w')

        # Update column and row weights to ensure resizing
        self.display_frame.grid_columnconfigure(1, weight=1)
        self.display_frame.grid_rowconfigure(6, weight=1)



    def copy_to_clipboard(self):
        query_text = self.query_text_display.get("1.0", tk.END).strip()
        pyperclip.copy(query_text)
        
    
    def new_query(self):
        messagebox.showinfo("New Query", "Create a new query.")
        
    def add_query(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add New Query")
        self.new_window.geometry("500x400")
        
        tk.Label(self.new_window, text="Title:").grid(row=0, column=0, pady=5)
        self.title_entry = tk.Entry(self.new_window)
        self.title_entry.grid(row=0, column=1, pady=5, sticky='ew')
        
        tk.Label(self.new_window, text="Author:").grid(row=1, column=0, pady=5)
        self.author_entry = tk.Entry(self.new_window)
        self.author_entry.grid(row=1, column=1, pady=5, sticky='ew')
        
        tk.Label(self.new_window, text="Description:").grid(row=2, column=0, pady=5)
        self.desc_text = tk.Text(self.new_window, height=5)
        self.desc_text.grid(row=2, column=1, pady=5, sticky='ew')
        
        tk.Label(self.new_window, text="Query:").grid(row=3, column=0, pady=5)
        self.query_text = tk.Text(self.new_window, height=10)
        self.query_text.grid(row=3, column=1, pady=5, sticky='ew')
        
        tk.Label(self.new_window, text="Tags (comma separated):").grid(row=4, column=0, pady=5)
        self.tags_entry = tk.Entry(self.new_window)
        self.tags_entry.grid(row=4, column=1, pady=5, sticky='ew')
        
        tk.Button(self.new_window, text="Save", command=self.save_query).grid(row=5, column=1, pady=10, sticky='e')
        
        # Make the new window resizable
        self.new_window.grid_columnconfigure(1, weight=1)
        self.new_window.grid_rowconfigure(2, weight=1)
        self.new_window.grid_rowconfigure(3, weight=2)
    
    def save_query(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        query_text = self.query_text.get("1.0", tk.END).strip()
        tags = self.tags_entry.get().strip()
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_favorite = 0

        # Check for duplicate title (case-insensitive)
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM queries WHERE LOWER(title) = LOWER(?)
        ''', (title,))
        count = cursor.fetchone()[0]
        if count > 0:
            messagebox.showwarning("Duplicate Title",
                                   "A KQL Query with the same title exists. You can paste your similar KQL Query to the Query Text field of the existing KQL Query Title, add few lines and paste :) Ostrich Algorithm Moment.")
            conn.close()
            return

        cursor.execute('''
        INSERT INTO queries (title, author, date_added, description, query_text, is_favorite, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, date_added, description, query_text, is_favorite, tags))

        conn.commit()
        conn.close()

        self.new_window.destroy()
        self.load_queries()

    
    def load_queries(self):
            # Clear the tree view
            for item in self.nav_tree.get_children():
                self.nav_tree.delete(item)

            # Load queries from the database and populate the navigation pane
            conn = sqlite3.connect('queries.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, title FROM queries WHERE title IS NOT NULL AND title != ""')
            rows = cursor.fetchall()

            for row in rows:
                self.nav_tree.insert('', 'end', row[0], text=row[1], values=(row[0],))

            conn.close()

    def export_data(self):
        file_types = [("CSV files", "*.csv"), ("JSON files", "*.json")]
        file_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension=file_types)
        if not file_path:
            return
        
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM queries')
        rows = cursor.fetchall()
        conn.close()
        
        if file_path.endswith('.csv'):
            self.export_to_csv(file_path, rows)
        elif file_path.endswith('.json'):
            self.export_to_json(file_path, rows)
    
    def export_to_csv(self, file_path, data):
        fieldnames = ['id', 'title', 'author', 'date_added', 'description', 'query_text', 'is_favorite', 'tags']
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow({
                    'id': row[0], 'title': row[1], 'author': row[2],
                    'date_added': row[3], 'description': row[4],
                    'query_text': row[5], 'is_favorite': row[6], 'tags': row[7]
                })

    def export_to_json(self, file_path, data):
        export_data = [
            {
                'id': row[0], 'title': row[1], 'author': row[2],
                'date_added': row[3], 'description': row[4],
                'query_text': row[5], 'is_favorite': row[6], 'tags': row[7]
            } for row in data
        ]
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=4)

    def import_data(self):
        file_types = [("CSV files", "*.csv"), ("JSON files", "*.json")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if not file_path:
            return
        
        if file_path.endswith('.csv'):
            self.import_from_csv(file_path)
        elif file_path.endswith('.json'):
            self.import_from_json(file_path)
    
    def import_from_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        self.validate_and_insert_data(data)
    
    def import_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
        self.validate_and_insert_data(data)

    
    def validate_and_insert_data(self, data):
        expected_fields = {'title', 'author', 'date_added', 'description', 'query_text', 'is_favorite', 'tags'}
        
        for entry in data:
            if not expected_fields.issubset(entry.keys()):
                messagebox.showerror("Import Error", "Invalid data format. Ensure all required fields are present.")
                return
        
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        
        for entry in data:
            try:
                cursor.execute('''
                INSERT INTO queries (title, author, date_added, description, query_text, is_favorite, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (entry['title'], entry['author'], entry['date_added'], entry['description'], entry['query_text'], entry['is_favorite'], entry['tags']))
            except sqlite3.IntegrityError:
                messagebox.showerror("Import Error", f"Failed to import query '{entry.get('title')}' due to integrity constraints.")
        
        conn.commit()
        conn.close()
        self.load_queries()



    
    def edit_query(self):
        selected_item = self.nav_tree.selection()
        if selected_item:
            query_id = self.nav_tree.item(selected_item[0], 'values')[0]
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Edit Query")
            self.edit_window.geometry("500x400")
            
            conn = sqlite3.connect('queries.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM queries WHERE id = ?', (query_id,))
            query = cursor.fetchone()
            conn.close()
            
            if query:
                tk.Label(self.edit_window, text="Title:").grid(row=0, column=0, pady=5)
                self.edit_title_entry = tk.Entry(self.edit_window)
                self.edit_title_entry.grid(row=0, column=1, pady=5, sticky='ew')
                self.edit_title_entry.insert(0, query[1])
                
                tk.Label(self.edit_window, text="Author:").grid(row=1, column=0, pady=5)
                self.edit_author_entry = tk.Entry(self.edit_window)
                self.edit_author_entry.grid(row=1, column=1, pady=5, sticky='ew')
                self.edit_author_entry.insert(0, query[2])
                
                tk.Label(self.edit_window, text="Description:").grid(row=2, column=0, pady=5)
                self.edit_desc_text = tk.Text(self.edit_window, height=5)
                self.edit_desc_text.grid(row=2, column=1, pady=5, sticky='ew')
                self.edit_desc_text.insert(tk.END, query[4])
                
                tk.Label(self.edit_window, text="Query:").grid(row=3, column=0, pady=5)
                self.edit_query_text = tk.Text(self.edit_window, height=10)
                self.edit_query_text.grid(row=3, column=1, pady=5, sticky='ew')
                self.edit_query_text.insert(tk.END, query[5])
                
                tk.Label(self.edit_window, text="Tags (comma separated):").grid(row=4, column=0, pady=5)
                self.edit_tags_entry = tk.Entry(self.edit_window)
                self.edit_tags_entry.grid(row=4, column=1, pady=5, sticky='ew')
                self.edit_tags_entry.insert(0, query[7])
                
                tk.Button(self.edit_window, text="Save Changes", command=lambda: self.save_edited_query(query_id)).grid(row=5, column=1, pady=10, sticky='e')
                
                # Make the edit window resizable
                self.edit_window.grid_columnconfigure(1, weight=1)
                self.edit_window.grid_rowconfigure(2, weight=1)
                self.edit_window.grid_rowconfigure(3, weight=2)
        else:
            messagebox.showwarning("No Selection", "Please select a query to edit.")
    
    def save_edited_query(self, query_id):
        title = self.edit_title_entry.get()
        author = self.edit_author_entry.get()
        description = self.edit_desc_text.get("1.0", tk.END).strip()
        query_text = self.edit_query_text.get("1.0", tk.END).strip()
        tags = self.edit_tags_entry.get().strip()
        
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE queries
        SET title = ?, author = ?, description = ?, query_text = ?, tags = ?
        WHERE id = ?
        ''', (title, author, description, query_text, tags, query_id))
        
        conn.commit()
        conn.close()
        
        self.edit_window.destroy()
        self.load_queries()
    
    def delete_query(self):
            selected_item = self.nav_tree.selection()
            if selected_item:
                query_id = self.nav_tree.item(selected_item[0], 'values')[0]
                query_title = self.nav_tree.item(selected_item[0], 'text')
                
                # Confirmation dialog
                confirm = messagebox.askyesno("Delete Query", f"Are you sure you want to delete the query '{query_title}'?")
                if confirm:
                    conn = sqlite3.connect('queries.db')
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM queries WHERE id = ?', (query_id,))
                    conn.commit()
                    conn.close()
                    self.load_queries()
            else:
                messagebox.showwarning("No Selection", "Please select a query to delete.")
    
    def search_query(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search Queries")

        tk.Label(self.search_window, text="Search Option:").grid(row=0, column=0, pady=5)
        self.search_option = ttk.Combobox(self.search_window, values=["Title", "Query Text", "Tags", "All"], state='readonly')
        self.search_option.set("All")
        self.search_option.grid(row=0, column=1, pady=5)

        tk.Label(self.search_window, text="Search Term:").grid(row=1, column=0, pady=5)
        self.search_entry = tk.Entry(self.search_window)
        self.search_entry.grid(row=1, column=1, pady=5)

        self.time_filter_var = tk.BooleanVar()
        tk.Checkbutton(self.search_window, text="Enable Time Range Filter", variable=self.time_filter_var, command=self.toggle_time_filter).grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(self.search_window, text="Start Date (YYYY-MM-DD HH:MM:SS):").grid(row=3, column=0, pady=5)
        self.start_date_entry = tk.Entry(self.search_window)
        self.start_date_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.search_window, text="End Date (YYYY-MM-DD HH:MM:SS):").grid(row=4, column=0, pady=5)
        self.end_date_entry = tk.Entry(self.search_window)
        self.end_date_entry.grid(row=4, column=1, pady=5)

        tk.Button(self.search_window, text="Search", command=self.perform_search).grid(row=5, column=1, pady=10)

        # Initially disable the time filter fields
        self.toggle_time_filter()


    def toggle_time_filter(self):
        state = 'normal' if self.time_filter_var.get() else 'disabled'
        self.start_date_entry.config(state=state)
        self.end_date_entry.config(state=state)



    def perform_search(self):
        search_term = self.search_entry.get()
        search_option = self.search_option.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        
        query = 'SELECT id, title FROM queries WHERE'
        params = []
        
        if search_option == "Title":
            query += ' title LIKE ?'
            params.append(f'%{search_term}%')
        elif search_option == "Query Text":
            query += ' query_text LIKE ?'
            params.append(f'%{search_term}%')
        elif search_option == "Tags":
            query += ' tags LIKE ?'
            params.append(f'%{search_term}%')
        else:  # All
            query += ' title LIKE ? OR query_text LIKE ? OR tags LIKE ?'
            params.extend([f'%{search_term}%'] * 3)
        
        if self.time_filter_var.get():
            if not start_date or not end_date:
                messagebox.showwarning("Time Filter Error", "Please enter both start and end dates.")
                return
            try:
                datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showwarning("Time Filter Error", "Invalid date format. Use YYYY-MM-DD HH:MM:SS.")
                return
            query += ' AND date_added BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        self.search_window.destroy()
        
        self.nav_tree.delete(*self.nav_tree.get_children())
        for row in rows:
            self.nav_tree.insert('', 'end', row[0], text=row[1], values=(row[0],))


if __name__ == "__main__":
    root = tk.Tk()
    app = QueryManagerApp(root)
    root.mainloop()