# Password Manager Software for Systems Security College Class

This work covers a password manager project developed with symmetric AES keys and PBE (Password-Based Encryption).

The goal is to enable an user to store her/his services' passwords in a encrypted PBE system, with a manageable and strong secret password. The first intention is to develop with Python language and then with Javascript.

![Password Manager Software Developed in htmlPy](https://raw.githubusercontent.com/davikawasaki/password-manager-security-class/master/imgs/pw-manager-list.png)

# TECHNOLOGIES & LIBRARIES USED

1) [Python 2.7](https://docs.python.org/2/)

2) [PyCrypto API 2.6](https://www.dlitz.net/software/pycrypto/api/2.6/)

3) [Jinja2](http://jinja.pocoo.org/docs/2.9/)

3) [Hashlib](https://docs.python.org/2/library/hashlib.html)

4) [re](https://docs.python.org/2/library/re.html)

5) [htmlPy](http://amol-mandhane.github.io/htmlPy/)

6) [jQuery](https://api.jquery.com/)

7) [Materialize](http://materializecss.com/getting-started.html)

# IMPLEMENTATION

Since the project needs to ensure data confidenciality and integrity, there aren't any secret (key or password) storage, because they encrypt/decrypt the data. Another thing necessary is the user's availability to reset her/his password in case of oblivion.

In order to meet with those requirements, the project uses the PBE methodology. The process, as used by [John Peñafiel](https://penafieljlm.com/2016/12/30/password-based-database-encryption/#problem-changing-passwords), follows these steps:

1\. When the user registers, the system provides a randomly generated recovery code, providing the user the ability to randomly generate a new set (password and a new recovery code) on demand, if she/he forgets her/his password;

2\. First is randomly generated an intermediary encryption key, which'll be used to encrypt a data;

3\. Then this encryption key is encrypted with a derivation of their password (using a Key Derivation Functions - KDF), which can be now stored in a AES encrypted file;

4\. Whenever there's a need to encrypt or decrypt some data, the user enter her/his password and run it through the same KDF;

5\. The password then is used to decrypt the encrypted intermediary encryption key, which will be used after decrypted to encrypt or decrypt user data.

6\. If the user forgets his password, she/he enters the recovery code passed on registration, which will do the same KDF process, which are represented below the password KDF fluxogram showed in the Figure below:

![Using Recovery Codes to Create Recoverable Copies of the Intermediate Key](https://raw.githubusercontent.com/davikawasaki/password-manager-security-class/master/imgs/crypt_pbe_recovery_questions.png)

# INSTALLATION

1\. Install htmlPy with pip:

```
$ [sudo] pip install htmlPy
```

2\. Install PySide library:

2.1\. In Windows:

```
$ pip install PySide
```

2.2\. In MacOS X:

```
$ brew install qt
or
$ pip install PySide
```

2.3\. In Linux:

```
$ sudo apt-get install python-pyside
```

3\. Install Jinja2 framework:

```
$ [sudo] pip install Jinja2
```

4\. After the packages installation, you need to set permissions to python/app/main.py to run:

```
$ chmod +x main.py
```

5\. Run the PW Manager with python 2.7:

```
$ ./main.py
```

# REFERENCES

1) [The Hitchhiker's Guide to Python - Cryptography](http://docs.python-guide.org/en/latest/scenarios/crypto/)

2) [Password-based Database Encryption](https://penafieljlm.com/2016/12/30/password-based-database-encryption/#problem-changing-passwords)

3) [Using Padding in Encryption](https://www.di-mgt.com.au/cryptopad.html)

# AUTHORS

This work is being developed to System Security undergrad-subject project. The people involved in the project are:

Student: POLETTO, André // polettoandre [at] gmail.com

Student: KAWASAKI, Davi // davishinjik [at] gmail.com

Student: BERTONCINI, João Vitor // joaobertoncini [at] alunos.utfpr.edu.br

Professor: YOKOYAMA, Roberto Sadao // yokoyama [at] utfpr.edu.br

# CONTACT & FEEDBACKS

Feel free to contact or pull request me to any relevant updates you may enquire:

KAWASAKI, Davi // davishinjik [at] gmail.com
