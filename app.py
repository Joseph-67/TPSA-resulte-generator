from desktop_app import TPSAApp, init_db


def main():
    init_db()
    app = TPSAApp()
    app.mainloop()


if __name__ == "__main__":
    main()
