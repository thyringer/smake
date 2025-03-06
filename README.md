# Cast 1.0

Cast is a CLI tool for reading strings or complex data sets from CSV files to output them in other text formats.

Cast can also be used as a CLI interface for xxHash to generate hash values.

## Outline of Functionalities

This Python script is a command line tool for generating SQL commands or other output with automatically hashed values using an algorithm of the xxHash family. The data to be processed is entered through the console or by reading in a text file. Furthermore, the printed results can be precisely formatted using templates.

When reading CSV files, the column names are available as placeholders within the template, which allows the data records to be automatically converted into a suitable SQL insert command, for instance. In fact, any use case that requires automatic conversion to another text file format is conceivable.

## CLI Setup

1. Install Python interpreter (at least version 3.9).
2. Satisfy dependency with `pip install xxhash`.

### Linux

1. Place program file `cast` (without Python extension `py`) under `~/local/bin` (Linux).

2. In the hidden file `.bashrc` located in the user's home directory, write the following line of code,

   `export PATH=$HOME/.local/bin:$PATH`

   if this search path for executable scripts is not yet known.
3. Make the script file executable with `chmod +x cast`.

## Usage

```bash
python cast <mode> <strings> [<options>]
```
Or if stored in the local or system-wide bin folder as `xxh`:

```bash
cast [<mode>] <strings> [<options>]
```

The first parameter specifies the algorithm, with the following options available:

- `   32` → `xxh32` 
- `   64` → `xxh64`
- ` 3_64` → `xxh3_64` 
- `3_128` → `xxh3_128`
- ` uuid` → hexadecimal digest of  `xxh3_128` formated as a UUID

In addition, each algorithm has a variant for a hexadecimal number `32x` and an unsigned integer `s32` as a result (which can be particularly useful in the context of PostgreSQL, since there are only signed integers available).

By default, `64` is assumed.

### Options

-  `--read` / `-r`

  Load file, where each line is treated as a string to be hashed. If a CSV file is present, the hash value is calculated from all columns separated by commas, unless `--input` is used to specify exactly which columns should be hashed and how. For this reason, the program assumes that CSV files have a table header.

- `--write` / `-w`

  Specify the file in which the results should be written instead of outputting them to the console. If the specified file does not yet exist, it will be created automatically.

- `--input` / `-i`

  Template with the placeholder `{string}`, which specifies how strings are to be hashed. When a CSV file is read in, individual column values can also be addressed using their column names as placeholders.

- `--output` / `-o`

  Template to specify exactly how records are to be output, with the possible placeholders `{string}`, `{input}`, `{hash}`, but also all column names of a read CSV file, where spaces between words are to be replaced by underscores. By default, `"{input}" => {hash}` is used as a template; for CSV files, however, an additional column for the generated hash values is added at the beginning.

- `--template` / `-t`

  The overall output can be defined using another template, where the placeholder `{records}` stands for all records.

- `--spacing` / `-s`

  This allows additional characters to be inserted between the individual records, by default a simple line break `"\n"`.

**Important Note**

In order for Bash to interpret line breaks as in `";\n"`, such strings must be written as `$';\n'`.

## Examples

Input with Default Settings:

```bash
cast 64 "Hello, world!" "This is a test string."
```

Output in Custom Format:

```bash
cast 64 "Hello, world!" "This is a test." -o "'{input}': {hash}"
```

**Generate an SQL insert command with records from a CSV data**

By specifying a template, an insert command can be generated:

```bash
cast 32s \
	-r capitals.csv \
	-w capitals.sql \
	-i "{country_code},{capital_city}" \
	-o "({hash}, '{country_code}', '{capital_city}')" \
	-t $'insert into City\n\t(hash, country, capital)\nvalues\n\t{records};\n' \
	-s $'\n\t' \
```

And with this CSV file as dataset,

```csv
capital city, country code, country
Washington D.C., US, United States
Ottawa, CA, Canada
Berlin, DE, Germany
Tokyo, JP, Japan
Canberra, AU, Australia
Paris, FR, France
Brasília, BR, Brazil
Moscow, RU, Russia
Beijing, CN, China
New Delhi, IN, India
```

the following output is generated:

```sql
insert into City
	(hash, country, capital)
values
	(1507852509, 'US', 'Washington D.C.')
	(2050315825, 'CA', 'Ottawa')
	(-1405512320, 'DE', 'Berlin')
	(1261058448, 'JP', 'Tokyo')
	(1366882969, 'AU', 'Canberra')
	(-1994286539, 'FR', 'Paris')
	(1797318940, 'BR', 'Brasília')
	(2116051181, 'RU', 'Moscow')
	(-711255517, 'CN', 'Beijing')
	(1246361623, 'IN', 'New Delhi');
```

## Dependencies

A Python interpreter version 3.9 or higher is expected. Furthermore, the following dependency must be installed using pip:

```bash
pip install xxhash
```

## License

Source code is public domain.
