package main

import "time"

type EmbedField struct {
	Name   string `json:"name"`
	Value  string `json:"value"`
	Inline bool   `json:"inline"`
}

type EmbedAuthor struct {
	Name    string `json:"name"`
	URL     string `json:"url"`
	IconURL string `json:"icon_url"`
}

type EmbedThumbnail struct {
	URL string `json:"url"`
}

type EmbedImage struct {
	URL string `json:"url"`
}

type EmbedFooter struct {
	Text    string `json:"text"`
	IconURL string `json:"icon_url"`
}

type Embed struct {
	Title       string         `json:"title"`
	Description string         `json:"description"`
	URL         string         `json:"url"`
	Color       int            `json:"color"`
	Fields      []EmbedField   `json:"fields"`
	Author      EmbedAuthor    `json:"author"`
	Thumbnail   EmbedThumbnail `json:"thumbnail"`
	Image       EmbedImage     `json:"image"`
	Footer      EmbedFooter    `json:"footer"`
	Timestamp   string         `json:"timestamp"`
}

type AllowedMentions struct {
	Parse []string `json:"parse"`
}

type DiscordMessage struct {
	Content         string          `json:"content"`
	Username        string          `json:"username"`
	Embeds          []Embed         `json:"embeds"`
	AllowedMentions AllowedMentions `json:"allowed_mentions"`
}

type MessageRequest struct {
	Title       string            `json:"title"`
	Description string            `json:"description"`
	AppName     string            `json:"app_name"`
	Color       int               `json:"color"`
	Timestamp   time.Time         `json:"timestamp"`
	Fields      map[string]string `json:"fields"`
}
