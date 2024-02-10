package main

import (
	"fmt"
	"os"
	"pacgobot/handlers"

	"github.com/bwmarrin/discordgo"
)

type BotHandler struct {
	Name        string
	Description string
	ShortHand   string
	HandlerFunc func(s *discordgo.Session, m *discordgo.MessageCreate)
}

var PREFIX = "p."

func main() {
	token := os.Getenv("BOT_TOKEN")
	if token == "" {
		fmt.Println("Error: BOT_TOKEN environment variable not set!")
		return
	}

	dg, err := discordgo.New("Bot " + token)
	if err != nil {
		fmt.Println("Error creating Discord session:", err)
		return
	}

	handlers.PREFIX = PREFIX
	BotMethods := []BotHandler{
		{
			Name:        "Avatar",
			Description: "Steals users's current avatar",
			ShortHand:   "av",
			HandlerFunc: handlers.AvatarHandler,
		},
		{
			Name:        "Ping",
			Description: "Ping to bot's backend server",
			ShortHand:   "ping",
			HandlerFunc: handlers.PingHandler,
		},
	}

	for _, funcs := range BotMethods {
		fmt.Printf("[INFO] Adding function %s\n", funcs.Name)
		dg.AddHandler(funcs.HandlerFunc)
	}

	err = dg.Open()
	if err != nil {
		fmt.Println("Error opening websocket connection:", err)
		return
	}

	fmt.Println("[INFO] Bot is now running. Press CTRL+C to exit.")
	<-make(chan struct{})
}
