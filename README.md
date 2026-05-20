# Relay

> Experimental Discord automation system developed under the Q-Verse Institute initiative.

Relay is a modular Discord bot focused on automation, utility features and experimental systems integration.

---

## Features

* Modular command system
* Utility commands
* Environment-based configuration
* Extensible architecture for future experiments

---

## Technology

* Python
* [discord.py](https://github.com/Rapptz/discord.py)
* Linux-oriented deployment workflow

---

## Documentation

Detailed command documentation is available in the project wiki.

---

## Setup

Clone the repository:

```bash
git clone https://github.com/Q-VerseInstitute/Relay.git
cd Relay
```

Create environment variables:

```bash
cp .env.example .env
```

Configure your [bot token](https://docs.discord.com/developers/platform/oauth2-and-permissions#bot-token):
```bash
vi .env
```
```bash
TOKEN={paste your token here}
...
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the bot:

```bash
python main.py
```

---

## Environment Variables

Example `.env` configuration:

```env
TOKEN=your_token_here
PREFIX=$
```

---

## Development Goals

- [ ] Improve modularity
- [ ] Expand functionality
- [ ] Containerized deployment
- [ ] Monitoring & logging improvements

---

## License

This project is licensed under the [MIT License](LICENSE).