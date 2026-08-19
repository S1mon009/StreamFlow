# Main module

The `main.py` module contains the application's entry point and high-level interaction loop.

## `main()`

The function:

1. clears the console;
2. creates a `VideoDownloader`;
3. collects download configuration;
4. asks the user to confirm;
5. starts the download;
6. asks whether another download should be performed.

## Running the module

The script can be executed directly:
```bsh
python main.py
```

The module uses the standard Python entry-point guard:
```py
if __name__ == "__main__":
    main()
```

## Class reference
:::main