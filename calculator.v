module calculator(suit1, number1, suit2, number2);
    input [1:0] suit1;
    input [3:0] number1;
    input [1:0] suit2;
    input [3:0] number2;

    parameter J = 3'd11;
    parameter Q = 3'd12;
    parameter K = 3'd13;
    parameter A = 3'd14;

    parameter SPADES = 2'd0;
    parameter HEARTS = 2'd1;
    parameter DIAMONDS = 2'd2;
    parameter CLUBS = 2'd3;
endmodule