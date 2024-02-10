package handlers

import (
	"fmt"
	"strings"

	"github.com/bwmarrin/discordgo"
)

type BotHandler struct {
	Name        string
	Description string
	ShortHand   string
	HandlerFunc func(s *discordgo.Session, m *discordgo.MessageCreate)
}

var PREFIX = ""

func AvatarHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
	if strings.HasPrefix(m.Content, PREFIX+"av") {
		toSteal := m.Author
		if len(m.Mentions) > 0 {
			toSteal = m.Mentions[0]
		}
		embed := &discordgo.MessageEmbed{
			Title: fmt.Sprintf("%s Persona", toSteal.Username),
			Color: 0x00FFFF,
			Image: &discordgo.MessageEmbedImage{
				URL: toSteal.AvatarURL("2048"),
			},
		}
		_, err := s.ChannelMessageSendEmbedReply(m.ChannelID, embed, m.Message.Reference())
		if err != nil {
			fmt.Println(err)
		}
	}
}

func PingHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Content == PREFIX+"ping" {
		s.ChannelMessageSend(m.ChannelID, fmt.Sprintf("```pong! %d ms```", s.HeartbeatLatency().Milliseconds()))
	}
}
