-- GreenBet — Schéma de base de données
-- Compatible MySQL 8+ et SQLite 3 (avec légères adaptations)

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pseudo VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('joueur', 'admin') DEFAULT 'joueur',
    solde_points INT DEFAULT 1000,
    statut ENUM('actif', 'banni') DEFAULT 'actif',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jeux (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    description TEXT,
    min_joueurs INT DEFAULT 1,
    max_joueurs INT DEFAULT 1,
    actif BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS parties (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    jeu_id INT NOT NULL,
    resultat ENUM('gagne', 'perdu', 'nul') NOT NULL,
    points_gagnes INT NOT NULL,
    joue_le DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (jeu_id) REFERENCES jeux(id)
);

-- Indexes for frequent lookups / filtering
CREATE INDEX IF NOT EXISTS idx_users_pseudo ON users(pseudo);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role_statut ON users(role, statut);
CREATE INDEX IF NOT EXISTS idx_jeux_nom_actif ON jeux(nom, actif);
CREATE INDEX IF NOT EXISTS idx_parties_user_date ON parties(user_id, joue_le);
CREATE INDEX IF NOT EXISTS idx_parties_jeu_date ON parties(jeu_id, joue_le);

-- Données initiales
INSERT INTO jeux (nom, description, min_joueurs, max_joueurs) VALUES
('Blackjack', 'Approchez 21 sans dépasser. Classique et sobre.', 1, 1),
('Roulette verte', 'Misez sur rouge, noir ou un numéro.', 1, 1),
('Poker simplifié', 'Main de 5 cartes, meilleure combinaison gagne.', 1, 1);

-- Compte admin par défaut (mot de passe : admin1234)
-- Remplacez <bcrypt_hash> par le vrai hash généré au premier lancement
-- Le hash ci-dessous est généré avec bcrypt.hashpw(b"admin1234", bcrypt.gensalt())
INSERT INTO users (pseudo, email, password_hash, role) VALUES
('admin', 'admin@greenbet.fr', '$2b$12$iUVnCg7WMDKlYhnElA6IE.eYAB/gJJ4yC7D4V.7vjYq0FvX5V0Wv6', 'admin');
