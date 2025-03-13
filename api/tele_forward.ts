import { VercelRequest, VercelResponse } from "@vercel/node";
import axios from "axios";

// Retrieve the environment variables
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TWILIO_WA_NUMBER = process.env.TWILIO_WA_NUMBER;
const RECIPIENT_WA_NUMBER = process.env.RECIPIENT_WA_NUMBER;
const TWILIO_SID = process.env.TWILIO_LIVE_SID;
const TWILIO_AUTH_TOKEN = process.env.TWILIO_LIVE_AUTH_TOKEN;

// Interface for the webhook request data
interface WebhookRequest {
  message: {
    text?: string;
  };
  sender?: string;
}

// The main handler function for the webhook
export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    const data: WebhookRequest = req.body;
    if (!data.message) {
      return res.status(400).json({ error: "No message in the webhook" });
    }

    const messageText = data.message.text || "New message received"; // Default text if no message text is available

    // Send message to WhatsApp via Twilio
    const twilioResponse = await axios.post(
      `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_SID}/Messages.json`,
      new URLSearchParams({
        From: `whatsapp:${TWILIO_WA_NUMBER}`,
        To: `whatsapp:${RECIPIENT_WA_NUMBER}`,
        Body: messageText,
      }).toString(),
      {
        auth: { username: TWILIO_SID!, password: TWILIO_AUTH_TOKEN! },
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }
    );

    console.log("Twilio Response:", twilioResponse.data);

    // Respond back with success
    return res.status(200).json({
      success: true,
      message: "Message forwarded to WhatsApp",
    });
  } catch (error: any) {
    console.error("Error processing webhook:", error);

    // Respond with an error status if something goes wrong
    return res.status(500).json({
      error: error.message || "Internal Server Error",
    });
  }
}
