/**
 * GreenBet — Poker simplifie (video poker)
 * 5 cartes, 1 tour d'echange, evaluation locale de la main.
 */
"use strict";

const SUITS = ["♠", "♥", "♦", "♣"];
const VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
const VALUE_TO_NUM = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, J: 11, Q: 12, K: 13, A: 14 };
const JEU_ID = 3;
const MISE = 50;

const PAYOUTS = {
  royal_flush: 300,
  straight_flush: 180,
  four_kind: 130,
  full_house: 90,
  flush: 70,
  straight: 60,
  three_kind: 45,
  two_pairs: 25,
  pair: 15,
  high_card: -MISE,
};

let deck = [];
let hand = [];
let held = new Set();
let canDraw = false;

const cardsEl = document.getElementById("poker-cards");
const rankEl = document.getElementById("poker-rank");
const helpEl = document.getElementById("poker-help");
const resultBanner = document.getElementById("result-banner");
const btnNew = document.getElementById("btn-new-hand");
const btnDraw = document.getElementById("btn-draw");
const btnReset = document.getElementById("btn-reset");
const soldeDisplay = document.getElementById("solde-display");

function buildDeck() {
  const d = [];
  for (const s of SUITS) for (const v of VALUES) d.push({ s, v });
  return d;
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function cardEl(card, idx) {
  const el = document.createElement("button");
  el.type = "button";
  el.className = "card-playing poker-card";
  el.dataset.idx = String(idx);
  if (["♥", "♦"].includes(card.s)) el.classList.add("rouge");
  else el.classList.add("noir");
  if (held.has(idx)) el.classList.add("is-held");
  el.innerHTML = `<span>${card.v}</span><span>${card.s}</span>`;
  el.disabled = !canDraw;
  return el;
}

function renderHand() {
  cardsEl.innerHTML = "";
  hand.forEach((card, idx) => cardsEl.appendChild(cardEl(card, idx)));
}

function countValues(values) {
  const m = {};
  for (const v of values) m[v] = (m[v] || 0) + 1;
  return Object.values(m).sort((a, b) => b - a);
}

function isStraight(sortedNums) {
  const uniq = [...new Set(sortedNums)];
  if (uniq.length !== 5) return false;
  const min = uniq[0];
  const max = uniq[4];
  if (max - min === 4) return true;
  return JSON.stringify(uniq) === JSON.stringify([2, 3, 4, 5, 14]);
}

function evaluateHand(cards) {
  const nums = cards.map(c => VALUE_TO_NUM[c.v]).sort((a, b) => a - b);
  const values = cards.map(c => c.v);
  const suits = cards.map(c => c.s);
  const counts = countValues(values);
  const flush = suits.every(s => s === suits[0]);
  const straight = isStraight(nums);
  const royal = JSON.stringify(nums) === JSON.stringify([10, 11, 12, 13, 14]);

  if (flush && royal) return { rank: "Quinte flush royale", key: "royal_flush" };
  if (flush && straight) return { rank: "Quinte flush", key: "straight_flush" };
  if (counts[0] === 4) return { rank: "Carré", key: "four_kind" };
  if (counts[0] === 3 && counts[1] === 2) return { rank: "Full", key: "full_house" };
  if (flush) return { rank: "Couleur", key: "flush" };
  if (straight) return { rank: "Suite", key: "straight" };
  if (counts[0] === 3) return { rank: "Brelan", key: "three_kind" };
  if (counts[0] === 2 && counts[1] === 2) return { rank: "Deux paires", key: "two_pairs" };
  if (counts[0] === 2) return { rank: "Une paire", key: "pair" };
  return { rank: "Carte haute", key: "high_card" };
}

function showResult(cls, msg) {
  resultBanner.className = `result-banner result-banner-poker ${cls} show`;
  resultBanner.textContent = msg;
}

function resetBanner() {
  resultBanner.className = "result-banner result-banner-poker";
  resultBanner.textContent = "";
}

function setControls({ newDisabled, drawDisabled, resetDisabled }) {
  btnNew.disabled = newDisabled;
  btnDraw.disabled = drawDisabled;
  btnReset.disabled = resetDisabled;
}

function startHand() {
  deck = shuffle(buildDeck());
  hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()];
  held = new Set();
  canDraw = true;

  rankEl.textContent = "Main initiale";
  helpEl.textContent = "Cliquez sur les cartes à conserver, puis appuyez sur “Échanger”.";
  resetBanner();
  renderHand();
  setControls({ newDisabled: false, drawDisabled: false, resetDisabled: false });
}

function toggleHold(idx) {
  if (!canDraw) return;
  if (held.has(idx)) held.delete(idx);
  else held.add(idx);
  renderHand();
}

function finishHand() {
  if (!canDraw) return;
  canDraw = false;
  setControls({ newDisabled: false, drawDisabled: true, resetDisabled: false });

  for (let i = 0; i < hand.length; i++) {
    if (!held.has(i)) hand[i] = deck.pop();
  }
  renderHand();

  const result = evaluateHand(hand);
  const pts = PAYOUTS[result.key];
  const resultat = pts > 0 ? "gagne" : "perdu";
  rankEl.textContent = result.rank;
  helpEl.textContent = "Nouvelle main pour rejouer.";
  showResult(resultat, `${result.rank} — ${pts > 0 ? "+" : ""}${pts} pts`);
  savePartie(resultat, pts);
}

function resetView() {
  deck = [];
  hand = [];
  held = new Set();
  canDraw = false;
  cardsEl.innerHTML = "";
  rankEl.textContent = "—";
  helpEl.textContent = "Cliquez sur “Nouvelle main” pour commencer.";
  resetBanner();
  setControls({ newDisabled: false, drawDisabled: true, resetDisabled: false });
}

function savePartie(resultat, points_gagnes) {
  fetch("/api/partie/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jeu_id: JEU_ID, resultat, points_gagnes }),
  })
    .then(r => r.json())
    .then(data => {
      if (data.new_solde !== undefined && soldeDisplay) soldeDisplay.textContent = data.new_solde;
      const soldeNav = document.getElementById("solde-nav");
      if (data.new_solde !== undefined && soldeNav) soldeNav.textContent = `${data.new_solde} pts`;
    })
    .catch(() => {});
}

cardsEl.addEventListener("click", (e) => {
  const target = e.target.closest(".poker-card");
  if (!target) return;
  toggleHold(Number(target.dataset.idx));
});
btnNew.addEventListener("click", startHand);
btnDraw.addEventListener("click", finishHand);
btnReset.addEventListener("click", resetView);

resetView();
