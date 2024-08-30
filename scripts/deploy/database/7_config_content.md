
- Look for the listen_addresses line. By default, it’s set to localhost. 

- Change it to * to allow PostgreSQL to listen on all available IP addresses.

```plaintext
listen_addresses = '*'
```
