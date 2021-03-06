/**
 * Contains all details about a Piece's move in the game.
 */

// DO NOT MODIFY THIS FILE
// Never try to directly create an instance of this class, or modify its member variables.
// Instead, you should only be reading its variables and calling its functions.

package games.chess;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import org.json.JSONObject;
import joueur.Client;
import joueur.BaseGame;
import joueur.BaseGameObject;

// <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
// you can add additional import(s) here
// <<-- /Creer-Merge: imports -->>

/**
 * Contains all details about a Piece's move in the game.
 */
public class Move extends GameObject {
    /**
     * The Piece captured by this Move, null if no capture.
     */
    public Piece captured;

    /**
     * The file the Piece moved from.
     */
    public String fromFile;

    /**
     * The rank the Piece moved from.
     */
    public int fromRank;

    /**
     * The Piece that was moved.
     */
    public Piece piece;

    /**
     * The Piece type this Move's Piece was promoted to from a Pawn, empty string if no promotion occurred.
     */
    public String promotion;

    /**
     * The standard algebraic notation (SAN) representation of the move.
     */
    public String san;

    /**
     * The file the Piece moved to.
     */
    public String toFile;

    /**
     * The rank the Piece moved to.
     */
    public int toRank;


    // <<-- Creer-Merge: fields -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    // you can add additional field(s) here. None of them will be tracked or updated by the server.
    // <<-- /Creer-Merge: fields -->>


    /**
     * Creates a new instance of a Move. Used during game initialization, do not call directly.
     */
    protected Move() {
        super();
    }

    // <<-- Creer-Merge: methods -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    // you can add additional method(s) here.
    // <<-- /Creer-Merge: methods -->>
}
