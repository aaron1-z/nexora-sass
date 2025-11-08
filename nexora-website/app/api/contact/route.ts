import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { name, email, organization, message } = body;

    // Validate required fields
    if (!name || !email || !message) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    // In a production environment, you would:
    // 1. Send email using Resend, SendGrid, or similar service
    // 2. Store the message in a database
    // 3. Send notifications to your team

    // For now, we'll just log the message
    console.log("Contact form submission:", {
      name,
      email,
      organization: organization || "N/A",
      message,
      timestamp: new Date().toISOString(),
    });

    // TODO: Integrate with email service
    // Example with Resend:
    // await resend.emails.send({
    //   from: 'contact@nexora.ai',
    //   to: 'hello@nexora.ai',
    //   subject: `Contact Form: ${name}`,
    //   html: `<p>From: ${name} (${email})${organization ? ` - ${organization}` : ''}</p><p>${message}</p>`
    // });

    return NextResponse.json(
      { message: "Message sent successfully" },
      { status: 200 }
    );
  } catch (error) {
    console.error("Contact form error:", error);
    return NextResponse.json(
      { error: "Failed to send message" },
      { status: 500 }
    );
  }
}

