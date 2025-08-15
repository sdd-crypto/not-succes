#!/usr/bin/env python3
import curses
import math
import threading
import time
import traceback
from dataclasses import dataclass
from typing import List, Tuple, Optional

import json
import requests


API_KEY = "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"
ENDPOINT = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar-pro"


@dataclass
class ChatMessage:
	role: str
	content: str


def call_perplexity_chat(messages: List[ChatMessage], temperature: float = 0.2, max_tokens: int = 1024, system_prompt: Optional[str] = None) -> str:
	if not API_KEY:
		raise RuntimeError("API key is missing. Please set API_KEY.")

	payload_messages = []
	if system_prompt:
		payload_messages.append({"role": "system", "content": system_prompt})
	for m in messages:
		payload_messages.append({"role": m.role, "content": m.content})

	headers = {
		"Authorization": f"Bearer {API_KEY}",
		"Content-Type": "application/json",
	}
	payload = {
		"model": MODEL,
		"temperature": temperature,
		"max_tokens": max_tokens,
		"messages": payload_messages,
	}
	resp = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload), timeout=60)
	resp.raise_for_status()
	data = resp.json()
	# Expected shape similar to OpenAI: choices[0].message.content
	try:
		return data["choices"][0]["message"]["content"]
	except Exception:
		return json.dumps(data, indent=2)


class RotatingCube:
	def __init__(self) -> None:
		self.points = [
			(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
			(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
		]
		self.edges = [
			(0, 1), (1, 2), (2, 3), (3, 0),
			(4, 5), (5, 6), (6, 7), (7, 4),
			(0, 4), (1, 5), (2, 6), (3, 7)
		]
		self.angle = 0.0

	def project(self, x: float, y: float, z: float, width: int, height: int, scale: float = 8.0) -> Tuple[int, int]:
		z += 5.0
		f = scale / (z if z != 0 else 1)
		x2 = int(width / 2 + x * f)
		y2 = int(height / 2 - y * f)
		return x2, y2

	def rotated_points(self) -> List[Tuple[float, float, float]]:
		ax = self.angle
		ay = self.angle * 0.7
		az = self.angle * 1.3

		sin_x, cos_x = math.sin(ax), math.cos(ax)
		sin_y, cos_y = math.sin(ay), math.cos(ay)
		sin_z, cos_z = math.sin(az), math.cos(az)

		rotated = []
		for (x, y, z) in self.points:
			# Rotate around X
			yx = y * cos_x - z * sin_x
			zx = y * sin_x + z * cos_x
			# Rotate around Y
			xy = x * cos_y + zx * sin_y
			zy = -x * sin_y + zx * cos_y
			# Rotate around Z
			xz = xy * cos_z - yx * sin_z
			yz = xy * sin_z + yx * cos_z
			rotated.append((xz, yz, zy))
		return rotated

	def step(self, delta: float) -> None:
		self.angle += delta
		if self.angle > math.tau:
			self.angle -= math.tau


class CursesApp:
	def __init__(self) -> None:
		self.screen = None
		self.height = 0
		self.width = 0
		self.running = True
		self.mode = "menu"  # menu | chat | planner
		self.chat_history: List[ChatMessage] = []
		self.output_lines: List[str] = []
		self.input_buffer: List[str] = []
		self.status_message: str = ""
		self.cube = RotatingCube()
		self.last_frame_time = time.time()

	def run(self) -> None:
		curses.wrapper(self._main)

	def _main(self, stdscr) -> None:
		self.screen = stdscr
		curses.curs_set(0)
		self.screen.nodelay(True)
		self.screen.timeout(30)
		self.height, self.width = self.screen.getmaxyx()

		while self.running:
			self._handle_resize()
			self._draw()
			self._handle_input()

		# Ensure the terminal cursor shows again
		curses.curs_set(1)

	def _handle_resize(self) -> None:
		h, w = self.screen.getmaxyx()
		if h != self.height or w != self.width:
			self.height, self.width = h, w
			self.screen.clear()

	def _draw(self) -> None:
		self.screen.erase()
		self._draw_header()
		self._draw_animation()
		if self.mode == "menu":
			self._draw_menu()
		elif self.mode == "chat":
			self._draw_chat()
		elif self.mode == "planner":
			self._draw_planner()
		self._draw_footer()
		self.screen.refresh()

	def _draw_header(self) -> None:
		title = "AI Security Assistant (Ethical) — 1) Chat  2) Security Planner  q) Quit"
		self.screen.addstr(0, 1, title[: max(0, self.width - 2)])
		if self.status_message:
			self.screen.addstr(1, 1, self.status_message[: max(0, self.width - 2)])
		else:
			self.screen.addstr(1, 1, "Use only on assets you own or have explicit permission to test.")

	def _draw_animation(self) -> None:
		# Reserve a small box in the top-right for the cube
		box_w = min(32, max(20, self.width // 4))
		box_h = 14
		start_y = 2
		start_x = max(0, self.width - box_w - 1)
		for x in range(start_x, start_x + box_w):
			if start_y < self.height:
				self.screen.addch(start_y, x, curses.ACS_HLINE)
			if start_y + box_h < self.height:
				self.screen.addch(start_y + box_h, x, curses.ACS_HLINE)
		for y in range(start_y, start_y + box_h + 1):
			if y < self.height and start_x < self.width:
				self.screen.addch(y, start_x, curses.ACS_VLINE)
			if y < self.height and start_x + box_w < self.width:
				self.screen.addch(y, start_x + box_w, curses.ACS_VLINE)
		if start_y < self.height and start_x < self.width:
			self.screen.addch(start_y, start_x, curses.ACS_ULCORNER)
		if start_y < self.height and start_x + box_w < self.width:
			self.screen.addch(start_y, start_x + box_w, curses.ACS_URCORNER)
		if start_y + box_h < self.height and start_x < self.width:
			self.screen.addch(start_y + box_h, start_x, curses.ACS_LLCORNER)
		if start_y + box_h < self.height and start_x + box_w < self.width:
			self.screen.addch(start_y + box_h, start_x + box_w, curses.ACS_LRCORNER)

		# Draw rotating cube inside the box
		now = time.time()
		delta = min(0.1, now - self.last_frame_time)
		self.last_frame_time = now
		self.cube.step(delta)
		rot = self.cube.rotated_points()
		# Translate drawing origin to box center
		center_x = start_x + box_w // 2
		center_y = start_y + box_h // 2
		# Project and draw edges
		projected = [self.cube.project(x, y, z, box_w, box_h) for (x, y, z) in rot]
		# Offset by box origin
		projected = [(center_x + (px - box_w // 2), center_y + (py - box_h // 2)) for (px, py) in projected]

		for (a, b) in self.cube.edges:
			x1, y1 = projected[a]
			x2, y2 = projected[b]
			self._draw_line(x1, y1, x2, y2)

	def _draw_line(self, x1: int, y1: int, x2: int, y2: int) -> None:
		# Bresenham's line algorithm
		dx = abs(x2 - x1)
		dy = -abs(y2 - y1)
		sx = 1 if x1 < x2 else -1
		sy = 1 if y1 < y2 else -1
		err = dx + dy
		x, y = x1, y1
		while True:
			if 0 <= x < self.width and 0 <= y < self.height:
				try:
					self.screen.addch(y, x, ord('*'))
				except curses.error:
					pass
			if x == x2 and y == y2:
				break
			e2 = 2 * err
			if e2 >= dy:
				err += dy
				x += sx
			if e2 <= dx:
				err += dx
				y += sy

	def _wrap_lines(self, lines: List[str], max_width: int) -> List[str]:
		wrapped: List[str] = []
		if max_width <= 0:
			return list(lines)
		for line in lines:
			if line == "":
				wrapped.append("")
				continue
			start = 0
			while start < len(line):
				wrapped.append(line[start : start + max_width])
				start += max_width
		return wrapped

	def _draw_menu(self) -> None:
		lines = [
			"Main Menu:",
			"1) AI Chat (Perplexity)",
			"2) Security Planner (Ethical, no active scanning)",
			"q) Quit",
		]
		for i, line in enumerate(lines):
			if 3 + i < self.height:
				self.screen.addstr(3 + i, 2, line[: max(0, self.width - 4)])

	def _draw_chat(self) -> None:
		start_y = 3
		max_lines = self.height - 8
		visible_messages = self._wrap_lines(self._chat_history_as_lines(), self.width - 4)
		visible_messages = visible_messages[-max_lines:]
		for i, line in enumerate(visible_messages):
			if start_y + i < self.height:
				self.screen.addstr(start_y + i, 2, line[: max(0, self.width - 4)])
		if self.height - 3 > 0:
			self.screen.addstr(self.height - 3, 2, "Type your message and press Enter. Press ESC to go back.")
		self._draw_input()

	def _draw_planner(self) -> None:
		start_y = 3
		text = [
			"Security Planner (Ethical)",
			"This mode will generate a SAFE, non-intrusive plan for assets you own or are authorized to test.",
			"It does NOT scan, exploit, or run commands.",
			"Enter a domain (you must be authorized):",
		]
		for i, line in enumerate(text):
			if start_y + i < self.height:
				self.screen.addstr(start_y + i, 2, line[: max(0, self.width - 4)])
		self._draw_input()
		# If we already have output_lines (last plan), render below
		if self.output_lines:
			self.screen.addstr(start_y + len(text) + 1, 2, "Plan:")
			wrapped = self._wrap_lines(self.output_lines, self.width - 4)
			visible = wrapped[: self.height - (start_y + len(text) + 3)]
			for i, line in enumerate(visible):
				row = start_y + len(text) + 2 + i
				if row < self.height:
					self.screen.addstr(row, 2, line[: max(0, self.width - 4)])

	def _draw_input(self) -> None:
		input_y = self.height - 2
		if input_y <= 2:
			return
		self.screen.addstr(input_y, 2, "> " + "".join(self.input_buffer)[: max(0, self.width - 6)])

	def _draw_footer(self) -> None:
		footer = "Press ESC to return to menu from a mode."
		if self.height - 1 >= 0:
			self.screen.addstr(self.height - 1, 1, footer[: max(0, self.width - 2)])

	def _handle_input(self) -> None:
		try:
			ch = self.screen.getch()
		except curses.error:
			ch = -1
		if ch == -1:
			return

		# Global keys
		if ch in (ord('q'), ord('Q')) and self.mode == "menu":
			self.running = False
			return
		if ch == 27:  # ESC
			self.mode = "menu"
			self.status_message = ""
			self.input_buffer = []
			return

		if self.mode == "menu":
			if ch == ord('1'):
				self.mode = "chat"
				self.status_message = "Chat mode."
				return
			if ch == ord('2'):
				self.mode = "planner"
				self.status_message = "Security Planner mode."
				self.output_lines = []
				self.input_buffer = []
				return
			return

		# Text input handling for modes
		if ch in (curses.KEY_BACKSPACE, 127, 8):
			if self.input_buffer:
				self.input_buffer.pop()
			return
		elif ch in (10, 13):  # Enter
			user_text = "".join(self.input_buffer).strip()
			self.input_buffer = []
			if not user_text:
				return
			if self.mode == "chat":
				self._submit_chat(user_text)
			elif self.mode == "planner":
				self._submit_planner(user_text)
			return
		else:
			# Append printable characters only
			if 32 <= ch <= 126:
				self.input_buffer.append(chr(ch))
			return

	def _chat_history_as_lines(self) -> List[str]:
		lines = []
		for msg in self.chat_history:
			prefix = "You: " if msg.role == "user" else "AI:  "
			for part in msg.content.splitlines() or [""]:
				lines.append(prefix + part)
		return lines

	def _append_output(self, text: str) -> None:
		for line in text.splitlines() or [""]:
			self.output_lines.append(line)

	def _submit_chat(self, text: str) -> None:
		self.chat_history.append(ChatMessage(role="user", content=text))
		self.status_message = "Thinking..."
		self._async_call(
			self._chat_call_worker,
			lambda: self._after_chat_call(),
		)

	def _chat_call_worker(self) -> None:
		try:
			response = call_perplexity_chat(self.chat_history)
			self.chat_history.append(ChatMessage(role="assistant", content=response))
		except Exception as e:
			self.chat_history.append(ChatMessage(role="assistant", content=f"Error: {e}\n{traceback.format_exc()}"))

	def _after_chat_call(self) -> None:
		self.status_message = ""

	def _submit_planner(self, domain: str) -> None:
		self.output_lines = []
		self.status_message = f"Planning for {domain}..."
		self._async_call(
			lambda: self._planner_call_worker(domain),
			lambda: self._after_planner_call(),
		)

	def _planner_call_worker(self, domain: str) -> None:
		prompt = (
			"You are an ethical security assistant. The user will provide a domain name they own or are authorized to test. "
			"Generate a SAFE, non-intrusive, step-by-step plan focusing on passive checks only (e.g., reviewing security headers, certificate transparency logs, "
			"public asset inventories, DNS records, and recommended manual checks). Do NOT perform or suggest active scanning, exploitation, brute force, fuzzing, "
			"or anything that could impact availability or integrity. Provide clear steps the user can follow themselves. Then outline how to set up a local lab "
			"with intentionally vulnerable targets (e.g., OWASP Broken Web Apps) for learning purposes."
		)
		messages = [ChatMessage(role="user", content=f"Domain: {domain}")]
		try:
			response = call_perplexity_chat(messages, system_prompt=prompt)
			self._append_output(response)
		except Exception as e:
			self._append_output(f"Error: {e}\n{traceback.format_exc()}")

	def _after_planner_call(self) -> None:
		self.status_message = ""

	def _async_call(self, worker, on_done) -> None:
		def runner():
			try:
				worker()
			finally:
				on_done()
		thread = threading.Thread(target=runner, daemon=True)
		thread.start()


def main() -> None:
	app = CursesApp()
	app.run()


if __name__ == "__main__":
	main()