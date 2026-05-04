/**
 * GreenBet — Blackjack vanilla JS
 * Green IT : zéro dépendance, zéro import, < 5 Ko
 */
"use strict";

const SUITS   = ["♠", "♥", "♦", "♣"];
const VALUES  = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
const JEU_ID  = 1;
const MISE    = 50;

let deck = [], playerHand = [], dealerHand = [], gameOver = false;

// ── DOM refs ──────────────────────────────────────────────────
const playerCardsEl  = document.getElementById("player-cards");
const dealerCardsEl  = document.getElementById("dealer-cards");
const playerScoreEl  = document.getElementById("player-score");
const dealerScoreEl  = document.getElementById("dealer-score");
const resultBanner   = document.getElementById("result-banner");
const btnDeal        = document.getElementById("btn-deal");
const btnHit         = document.getElementById("btn-hit");
const btnStand       = document.getElementById("btn-stand");
const soldeDisplay   = document.getElementById("solde-display");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ── Deck helpers ──────────────────────────────────────────────
function buildDeck() {
  const d = [];
  for (const s of SUITS) for (const v of VALUES) d.push({ s, v });
  return d;
}

/** Fisher-Yates shuffle */
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function cardValue(card) {
  if (["J", "Q", "K"].includes(card.v)) return 10;
  if (card.v === "A") return 11;
  return parseInt(card.v, 10);
}

function handTotal(hand) {
  let total = 0, aces = 0;
  for (const c of hand) {
    total += cardValue(c);
    if (c.v === "A") aces++;
  }
  while (total > 21 && aces > 0) { total -= 10; aces--; }
  return total;
}

// ── Render ────────────────────────────────────────────────────
function cardEl(card, hidden = false) {
  const el = document.createElement("div");
  el.className = "card-playing";
  if (hidden) {
    el.className += " card-hidden";
  } else {
    el.className += (["♥","♦"].includes(card.s) ? " rouge" : " noir");
    el.innerHTML = `<span>${card.v}</span><span>${card.s}</span>`;
  }
  return el;
}

function renderHands(revealDealer = false) {
  playerScoreEl.textContent = handTotal(playerHand);
  while (playerCardsEl.children.length < playerHand.length) {
    const idx = playerCardsEl.children.length;
    const el = cardEl(playerHand[idx]);
    el.classList.add("card-enter");
    if (idx === 0) el.style.animationDelay = "0s";
    else if (idx === 1) el.style.animationDelay = "0.2s";
    playerCardsEl.appendChild(el);
  }

  dealerScoreEl.textContent = revealDealer ? handTotal(dealerHand) : "?";
  while (dealerCardsEl.children.length < dealerHand.length) {
    const idx = dealerCardsEl.children.length;
    const hidden = (idx === 1 && !revealDealer);
    const el = cardEl(dealerHand[idx], hidden);
    el.classList.add("card-enter");
    if (idx === 0) el.style.animationDelay = "0.1s";
    else if (idx === 1) el.style.animationDelay = "0.3s";
    dealerCardsEl.appendChild(el);
  }

  if (revealDealer && dealerHand.length >= 2) {
    const card2 = dealerCardsEl.children[1];
    if (card2.classList.contains("card-hidden")) {
      card2.classList.remove("card-hidden");
      const isRouge = ["♥","♦"].includes(dealerHand[1].s);
      card2.classList.add(isRouge ? "rouge" : "noir");
      card2.classList.add("card-flip");
      
      setTimeout(() => {
        card2.innerHTML = `<span>${dealerHand[1].v}</span><span>${dealerHand[1].s}</span>`;
      }, 150);
    }
  }
}

// ── Game logic ────────────────────────────────────────────────
function deal() {
  deck = shuffle(buildDeck());
  playerHand = [deck.pop(), deck.pop()];
  dealerHand = [deck.pop(), deck.pop()];
  gameOver = false;

  hideResult();
  
  playerCardsEl.innerHTML = "";
  dealerCardsEl.innerHTML = "";
  
  renderHands(false);
  btnHit.disabled = false;
  btnStand.disabled = false;
  btnDeal.textContent = "Recommencer";

  if (handTotal(playerHand) === 21) stand();
}

function hit() {
  if (gameOver) return;
  playerHand.push(deck.pop());
  if (handTotal(playerHand) > 21) {
    renderHands(true);
    endGame("perdu", "Vous avez dépassé 21 !");
  } else {
    renderHands(false);
  }
}

async function stand() {
  if (gameOver) return;
  btnHit.disabled = true;
  btnStand.disabled = true;

  showSuspense("Le croupier reflechit...");
  await sleep(900);
  showSuspense("Le croupier revele sa carte...");
  await sleep(1200);
  renderHands(true);
  await sleep(1400);

  while (handTotal(dealerHand) < 17) {
    showSuspense("Le croupier hesite...");
    await sleep(800 + Math.floor(Math.random() * 400));
    showSuspense("Le croupier tire une carte...");
    await sleep(1300 + Math.floor(Math.random() * 600));
    dealerHand.push(deck.pop());
    renderHands(true);
    await sleep(1700);
  }

  const p = handTotal(playerHand), d = handTotal(dealerHand);
  if (d > 21 || p > d)      endGame("gagne", `Vous gagnez ! (${p} vs ${d})`);
  else if (p < d)            endGame("perdu", `Croupier gagne (${d} vs ${p})`);
  else                       endGame("nul",   `Egalite (${p})`);
}

function endGame(resultat, msg) {
  gameOver = true;
  btnHit.disabled = true;
  btnStand.disabled = true;

  const pts = resultat === "gagne" ? MISE : resultat === "perdu" ? -MISE : 0;
  showResult(resultat, `${msg} ${pts >= 0 ? "+" : ""}${pts} pts`);
  savePartie(resultat, pts);
}

// ── Result banner ─────────────────────────────────────────────
function showResult(cls, msg) {
  resultBanner.className = `result-banner ${cls} show`;
  resultBanner.textContent = msg;
}
function hideResult() {
  resultBanner.className = "result-banner";
  resultBanner.textContent = "";
}

function showSuspense(msg) {
  resultBanner.className = "result-banner suspense show";
  resultBanner.textContent = msg;
}

// ── API ───────────────────────────────────────────────────────
function savePartie(resultat, points_gagnes) {
  fetch("/api/partie/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jeu_id: JEU_ID, resultat, points_gagnes }),
  })
    .then(r => r.json())
    .then(data => {
      if (data.new_solde !== undefined && soldeDisplay) {
        soldeDisplay.textContent = data.new_solde;
      }
      const soldeNav = document.getElementById("solde-nav");
      if (data.new_solde !== undefined && soldeNav) {
        soldeNav.textContent = `${data.new_solde} pts`;
      }
    })
    .catch(() => {});
}

// ── Events ────────────────────────────────────────────────────
btnDeal.addEventListener("click", deal);
btnHit.addEventListener("click", hit);
btnStand.addEventListener("click", stand);
