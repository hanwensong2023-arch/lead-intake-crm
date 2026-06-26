import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Lead Intake CRM",
  description: "Public lead intake and internal attorney follow-up workflow"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <header className="topbar">
            <Link className="brand" href="/">
              Lead Intake CRM
            </Link>
            <nav className="nav" aria-label="Primary">
              <Link href="/">Public form</Link>
              <Link href="/register">Attorney registration</Link>
              <Link href="/leads">Internal leads</Link>
              <Link href="/admin/attorneys">Attorney management</Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
