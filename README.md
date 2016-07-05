## About FixUserDb

When analyzing files, one of the information we need to know
at first is it's compiler or packer signature. Some tools like
PEID or exeinfo PE use a public signature format and save them
in a plaintext file "userdb.txt".
However, there are lots of invalid entries inside after being
modified by researchers or public users years after years. So
I write this utility to help you to remove those invalid entries.



###Main features:
- Remove entry that already has the same signature and section name previously.
- Remove entry that has invalid signature which is neither hex nor ? format.



## Author
[ChienWei Hung] (https://www.linkedin.com/profile/view?id=351402223)
